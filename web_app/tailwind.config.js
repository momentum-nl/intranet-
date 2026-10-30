/** Momentum-huisstijl: kleuren als rgb-tripletten in static/src/app.css. */
const v = (n) => `rgb(var(--color-${n}) / <alpha-value>)`;
module.exports = {
  content: ["./templates/**/*.html", "./apps/**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: v("primary"), hover: v("primary-hover"), light: v("primary-light") },
        secondary: { DEFAULT: v("secondary"), light: v("secondary-light") },
        warm: { DEFAULT: v("warm"), light: v("warm-light"), hero: v("warm-hero") },
        deep: v("deep"),
        peach: { 50: v("peach-50"), 200: v("peach-200"), 900: v("peach-900") },
        sunset: { 50: v("sunset-50") },
        wgrey: v("wgrey"),
        grey: { DEFAULT: v("grey"), 300: v("grey-300") },
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
        sans: ["Aeonik", "Inter", "system-ui", "sans-serif"],
        display: ["Aeonik", "Inter", "system-ui", "sans-serif"],
        serif: ["SourceSerif4", "Georgia", "serif"],
      },
    },
  },
};
