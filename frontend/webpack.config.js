var path = require('path');
var webpack = require('webpack');
var merge = require('webpack-merge');

var TARGET = process.env.NODE_ENV;

var common = {
  resolve: {
    // root: [path.resolve("./bower_components")],
    modulesDirectories: ["node_modules", "bower_components"]
  },
  entry: [
    'webpack-dev-server/client?http://0.0.0.0:3000',
    'webpack/hot/only-dev-server',
    './src/index'
  ],
  output: {
    path: path.join(__dirname, 'build', 'js'),
    filename: 'bundle.js',
    publicPath: 'http://localhost:3000/build/js/'
  },
  plugins: [
    new webpack.ResolverPlugin(
      new webpack.ResolverPlugin.DirectoryDescriptionFilePlugin(
        ".bower.json", ["main"], ["normal", "loader"])
    ),
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.NoErrorsPlugin(),
  ],
  module: {
    loaders: [{
        test: /\.js$/,
        include: __dirname,
        exclude: /node_modules/,
        loader: 'babel',
        query: {
          presets: ['react', 'es2015']
        }
      }
    ]
  }
};

if (TARGET === 'dev') {
  module.exports = merge(common, {
    devtool: 'cheap-module-eval-source-map',
    plugins: [
      new webpack.HotModuleReplacementPlugin()
    ],
    module: {
      loaders: [{
        test: /\.js$/,
        include: __dirname,
        exclude: /node_modules/,
        loaders: ['react-hot', 'babel']
      }]
    }

  });
};

if (TARGET === 'prod') {
  module.exports = merge(common, {
    plugins: [
      new webpack.optimize.DedupePlugin(),
      new webpack.optimize.AggressiveMergingPlugin(),
      new webpack.optimize.UglifyJsPlugin({
        mangle: {
          screw_ie8: true
        },
        compress: {
          sequences: true,
          dead_code: true,
          conditionals: true,
          booleans: true,
          unused: true,
          if_return: true,
          join_vars: true,
          drop_console: true
        }
      })
    ]
  });
}
