// tailwind.config.js
module.exports = {
  content: [
    './core/templates/**/*.html',
    './core/static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'hacker': {
          green: '#00FF41',
          dark: '#0a0a0a',
          black: '#000000',
          light: '#33ff33',
        }
      },
      fontFamily: {
        'mono': ['Vazir Code', 'Courier New', 'monospace'],
      }
    },
  },
  plugins: [],
}