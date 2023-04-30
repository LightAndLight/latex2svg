define(
  `math_block',
  `dnl
esyscmd(`echo "'patsubst($1, `\\', `\\\\')`" | texmath -f tex -t mathml')dnl
')dnl
define(
  `math_inline',
  `dnl
esyscmd(`echo "'patsubst($1, `\\', `\\\\')`" | texmath --inline -f tex -t mathml')dnl
')
