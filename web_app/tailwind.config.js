/** Momentum-huisstijl: kleuren als rgb-tripletten in static/src/app.css. */
const v = (n) => `rgb(var(--color-${n}) / <alpha-value>)`;
module.exports = {
  content: ["./templates/**/*.html", "./apps/**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: v("primary"), hover: v("primary-hover"), light: v("primary-light") },
        secondary: { DEFAULT: v("secondary"), light: v("secondary-light") },
        warm: { DEFAULT: v("warm"), light: v("warm-light") },
        danger: { DEFAULT: v("danger"), light: v("danger-light") },
        success: v("success"),
        warning: v("warning"),
        ink: v("text-primary"),
        muted: v("text-muted"),
        line: v("border"),
        canvas: v("bg-secondary"),
        surface: v("bg-primary"),
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Poppins", "Inter", "sans-serif"],
      },
    },
  },
};
