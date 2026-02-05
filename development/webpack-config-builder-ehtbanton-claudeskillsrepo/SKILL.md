---
name: webpack-config-builder
description: Generate Webpack configuration files for bundling JavaScript/TypeScript applications with loaders, plugins, and optimization settings. Triggers on "create webpack config", "generate webpack configuration", "webpack setup for", "bundle config".
---

# Webpack Config Builder

Generate production-ready Webpack configuration files with appropriate loaders, plugins, and optimization settings.

## Output Requirements

**File Output:** `webpack.config.js` or `webpack.config.ts`
**Format:** Valid Webpack 5 configuration
**Standards:** Webpack 5.x

## When Invoked

Immediately generate a complete Webpack configuration with development and production modes, loaders for common file types, and optimization settings.

## Configuration Template

```javascript
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = (env, argv) => {
  const isProduction = argv.mode === 'production';

  return {
    entry: './src/index.tsx',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: isProduction ? '[name].[contenthash].js' : '[name].js',
      clean: true,
    },
    resolve: {
      extensions: ['.tsx', '.ts', '.js'],
      alias: { '@': path.resolve(__dirname, 'src') },
    },
    module: {
      rules: [
        {
          test: /\.tsx?$/,
          use: 'ts-loader',
          exclude: /node_modules/,
        },
        {
          test: /\.css$/,
          use: [isProduction ? MiniCssExtractPlugin.loader : 'style-loader', 'css-loader'],
        },
      ],
    },
    plugins: [
      new HtmlWebpackPlugin({ template: './public/index.html' }),
      isProduction && new MiniCssExtractPlugin(),
    ].filter(Boolean),
    devServer: {
      port: 3000,
      hot: true,
    },
  };
};
```

## Example Invocations

**Prompt:** "Create webpack config for React TypeScript"
**Output:** Complete `webpack.config.js` with TypeScript, React, CSS support.
