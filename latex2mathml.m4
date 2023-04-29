define(
  `m4_eq',
  `dnl
esyscmd(`echo "'patsubst($1, `\\', `\\\\')`" | texmath -f tex -t mathml')dnl
')
