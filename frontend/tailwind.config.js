/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class', // This enables dark mode based on a CSS class
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: '#222',
        darkText: '#fff',
        lightBg: '#fff',
        lightText: '#333',
      },
    },
  },
  plugins: [],
}

