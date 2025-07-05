/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html"

  ],
    safelist: [
    'grid-cols-1',
    'grid-cols-2',
    'grid-cols-3',
    'grid-cols-4',
    'grid',
    'sm:grid-cols-4',
    'md:grid-cols-4',
    'lg:grid-cols-4',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

