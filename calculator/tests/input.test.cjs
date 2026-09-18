const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const vm = require('node:vm');

// 执行页面中的真实脚本，DOM 替身只提供显示所需的接口。
const html = readFileSync(join(__dirname, '../index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
function calculator() {
  const elements = Object.fromEntries(['display', 'curr', 'expr'].map(id =>
    [id, { textContent: '', classList: { toggle() {} } }]));
  const context = vm.createContext({
    document: { getElementById: id => elements[id] },
    setTimeout: () => 0,
  });
  vm.runInContext(script, context);
  return {
    press(keys) {
      for (const key of keys) {
        if (key === 'C') context.clearAll();
        else if (key === '<') context.backspace();
        else if (key === '=') context.equal();
        else if ('+-*/'.includes(key)) context.inputOp(key);
        else context.inputDigit(key);
      }
    },
    display: () => String(elements.curr.textContent),
    expression: () => elements.expr.textContent,
    context,
  };
}

const cases = [
  ['初始显示', '', '0'],
  ['多位小数', '12.5', '12.5'],
  ['重复小数点', '1..2...', '1.2'],
  ['小数点开头', '.5', '0.5'],
  ['前导零', '00012', '12'],
  ['保留小数末尾零', '0.00', '0.00'],
  ['退格保留小数点', '12.5<', '12.'],
  ['删除小数点后可重新输入', '12.<<.5', '1.5'],
  ['连续退格到空', '1<<<', '0'],
  ['清除后重新输入', '12.5C7', '7'],
  ['两个操作数均支持小数', '1.2+3.4=', '4.6'],
  ['第二个操作数删空', '12+3<', '0'],
  ['删空后等号不计算', '12+3<=', '0'],
  ['删空后重新输入', '12+3<4=', '16'],
  ['显式输入零参与运算', '12+0=', '12'],
  ['结果后直接输入开启新计算', '2+3=7', '7'],
  ['结果后输入小数点开启新计算', '2+3=.5', '0.5'],
  ['结果后选择运算符继续计算', '2+3=+4=', '9'],
  ['切换运算符', '12+-3=', '9'],
  ['连续等号保持原行为', '5+3===', '14'],
  ['清除待计算状态', '12+3C4=', '4'],
  ['清除重复等号状态', '5+3=C2=', '2'],
  ['错误后清除', '1/0C2', '2'],
  ['结果后退格保持原行为', '2+3=<', '5'],
];
for (const [name, keys, expected] of cases) {
  test(name, () => {
    const calc = calculator();
    calc.press(keys);
    assert.equal(calc.display(), expected);
  });
}
test('非法输入不破坏结果及后续计算', () => {
  const calc = calculator();
  calc.press('2+3=');
  for (const value of ['', '12', 'x', null, undefined, 2]) calc.context.inputDigit(value);
  assert.equal(calc.display(), '5');
  calc.press('+4=');
  assert.equal(calc.display(), '9');
});
test('清除同时清空表达式', () => {
  const calc = calculator();
  calc.press('12+3C');
  assert.equal(calc.display(), '0');
  assert.equal(calc.expression(), '');
});
