const prettier = require('eslint-plugin-prettier');

module.exports = [
  {
    rules: {},
  },
  {
    plugins: {
      prettier: prettier,
    },
    rules: {
      'prettier/prettier': ['error'],
    },
  },
];
