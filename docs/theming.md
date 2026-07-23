# Theming Guide — Choose Your UI

This blog uses [Astro](https://astro.build) as the framework. You can either use an existing theme or build your own with a UI component library.

---

## Option 1 — Ready-made Astro Themes (fastest)

Pick one and follow its README to install.

| Theme | Style | Docs |
|-------|-------|------|
| [AstroPaper](https://github.com/satnaing/astro-paper) | Minimal, dark/light, built-in search | [Demo](https://astro-paper.pages.dev) |
| [Astro Nano](https://github.com/markhorn-dev/astro-nano) | Ultra-minimal, zero JS by default | [Demo](https://astro-nano-demo.vercel.app) |
| [Astro Wind](https://github.com/onwidget/astrowind) | Landing page + blog, Tailwind | [Demo](https://astrowind.vercel.app) |
| [Accessible Astro Starter](https://github.com/markteekman/accessible-astro-starter) | Accessibility-first | [Demo](https://starter.accessible-astro.dev) |

### How to install a theme

```bash
# Option A — use the theme's own template
npm create astro@latest -- --template satnaing/astro-paper

# Option B — clone manually
git clone https://github.com/satnaing/astro-paper.git my-blog
cd my-blog
npm install
```

---

## Option 2 — UI Component Libraries (more control)

Build on top of plain Astro with a component library of your choice.

### Tailwind CSS

The most popular choice for Astro blogs. Utility-first, no component opinions.

- Docs: [tailwindcss.com](https://tailwindcss.com/docs/installation)
- Astro integration: [docs.astro.build/en/guides/integrations-guide/tailwind](https://docs.astro.build/en/guides/integrations-guide/tailwind/)

```bash
npx astro add tailwind
```

### shadcn/ui

Unstyled, accessible components built on Radix UI. Works with React inside Astro.

- Docs: [ui.shadcn.com](https://ui.shadcn.com/docs/installation/astro)

```bash
npx astro add react
npx shadcn@latest init
```

### Daisy UI

Tailwind-based component library with pre-made themes (dark, cupcake, cyberpunk, etc).

- Docs: [daisyui.com](https://daisyui.com/docs/install/)

```bash
npm install daisyui
```

Then add to `tailwind.config.mjs`:
```js
plugins: [require("daisyui")]
```

### Flowbite

Tailwind component library with a large component set.

- Docs: [flowbite.com/docs/getting-started/astro](https://flowbite.com/docs/getting-started/astro/)

```bash
npm install flowbite
```

---

## Option 3 — Build from scratch

If you prefer full control with no dependencies:

```bash
npm create astro@latest my-blog
# Select "Empty" template
# Add only what you need
```

Astro docs for content collections (blog posts): [docs.astro.build/en/guides/content-collections](https://docs.astro.build/en/guides/content-collections/)

---

## Connecting to the quiz pipeline

Regardless of which theme you choose, the quiz pipeline only requires:

1. Posts live in `src/content/posts/` as `.md` or `.mdx` files
2. Drafts live in `drafts/` before publishing
3. The Astro build command is `pnpm build` (or `npm run build`)

The GitHub Actions workflows in `.github/workflows/` handle moving files from `drafts/` → `src/content/posts/` automatically on publish.
