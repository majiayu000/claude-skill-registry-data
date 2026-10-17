---
name: figma-portfolio-nextjs
description: Build and customize a modern developer/designer portfolio with Next.js, TypeScript, and TailwindCSS featuring animated typing effects and responsive layouts.
triggers:
  - create a portfolio website
  - build a developer portfolio with nextjs
  - customize figma portfolio template
  - add projects to portfolio site
  - setup personal portfolio with tailwind
  - configure nextjs portfolio animations
  - deploy portfolio to vercel
  - modify portfolio hero section
---

# Figma Portfolio - Next.js Developer Portfolio

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A personal portfolio template for developers and designers, built with Next.js 16, TypeScript, and TailwindCSS. Features a clean dark-themed UI with purple gradient accents, animated typing effects, responsive layouts, and sections to showcase projects, experience, and creative skills.

## Installation

```bash
# Clone the repository
git clone git@github.com:ibrahimmemonn/Figma_Portfolio.git

# Navigate to project directory
cd Figma_Portfolio/

# Install dependencies
npm install

# Run development server
npm run dev
```

The development server starts at `http://localhost:3000`.

## Project Structure

```
Figma_Portfolio/
├── app/
│   ├── page.tsx           # Main landing page
│   ├── layout.tsx         # Root layout with font config
│   └── globals.css        # Global styles with Tailwind
├── components/
│   ├── Hero.tsx           # Hero section with typing animation
│   ├── Projects.tsx       # Project showcase section
│   ├── Experience.tsx     # Experience timeline
│   ├── Skills.tsx         # Skills display
│   └── Contact.tsx        # Contact section
├── public/
│   ├── projects/          # Project images
│   └── assets/            # Icons and media
└── tailwind.config.ts     # Tailwind configuration
```

## Key Features & Configuration

### Font Configuration

The portfolio uses Poppins font optimized with `next/font`:

```typescript
// app/layout.tsx
import { Poppins } from 'next/font/google';

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700', '800', '900'],
  variable: '--font-poppins',
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={poppins.variable}>
      <body>{children}</body>
    </html>
  );
}
```

### Hero Section with Typing Animation

```typescript
// components/Hero.tsx
'use client';
import { useState, useEffect } from 'react';

export default function Hero() {
  const [text, setText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);
  const [loopNum, setLoopNum] = useState(0);
  const [typingSpeed, setTypingSpeed] = useState(150);

  const roles = ['Software Engineer', 'UI/UX Designer', 'Full Stack Developer'];

  useEffect(() => {
    const handleType = () => {
      const i = loopNum % roles.length;
      const fullText = roles[i];

      setText(
        isDeleting
          ? fullText.substring(0, text.length - 1)
          : fullText.substring(0, text.length + 1)
      );

      setTypingSpeed(isDeleting ? 50 : 150);

      if (!isDeleting && text === fullText) {
        setTimeout(() => setIsDeleting(true), 1000);
      } else if (isDeleting && text === '') {
        setIsDeleting(false);
        setLoopNum(loopNum + 1);
      }
    };

    const timer = setTimeout(handleType, typingSpeed);
    return () => clearTimeout(timer);
  }, [text, isDeleting, loopNum, typingSpeed, roles]);

  return (
    <section className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-5xl md:text-7xl font-bold mb-6">
          Hi, I'm <span className="bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">Your Name</span>
        </h1>
        <h2 className="text-2xl md:text-4xl mb-8">
          <span className="text-gray-400">{text}</span>
          <span className="animate-pulse">|</span>
        </h2>
        <p className="text-gray-300 text-lg max-w-2xl mx-auto">
          Building digital experiences that combine aesthetic design with powerful functionality.
        </p>
      </div>
    </section>
  );
}
```

### Adding Projects

```typescript
// components/Projects.tsx
interface Project {
  title: string;
  description: string;
  image: string;
  link: string;
  github?: string;
  tags: string[];
}

const projects: Project[] = [
  {
    title: 'E-Commerce Platform',
    description: 'Full-stack e-commerce solution with Next.js, Stripe, and MongoDB',
    image: '/projects/ecommerce.png',
    link: 'https://example.com',
    github: 'https://github.com/username/project',
    tags: ['Next.js', 'TypeScript', 'Stripe', 'MongoDB'],
  },
  {
    title: 'Portfolio Dashboard',
    description: 'Analytics dashboard for tracking portfolio metrics',
    image: '/projects/dashboard.png',
    link: 'https://example.com',
    tags: ['React', 'Chart.js', 'TailwindCSS'],
  },
];

export default function Projects() {
  return (
    <section className="py-20 px-4">
      <h2 className="text-4xl font-bold text-center mb-12">
        Featured <span className="bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">Projects</span>
      </h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {projects.map((project, index) => (
          <div key={index} className="bg-gray-800/50 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-all duration-300">
            <img src={project.image} alt={project.title} className="w-full h-48 object-cover" />
            <div className="p-6">
              <h3 className="text-xl font-semibold mb-2">{project.title}</h3>
              <p className="text-gray-400 mb-4">{project.description}</p>
              <div className="flex flex-wrap gap-2 mb-4">
                {project.tags.map((tag, i) => (
                  <span key={i} className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-sm">
                    {tag}
                  </span>
                ))}
              </div>
              <div className="flex gap-4">
                <a href={project.link} className="text-purple-400 hover:text-purple-300">
                  Live Demo →
                </a>
                {project.github && (
                  <a href={project.github} className="text-gray-400 hover:text-gray-300">
                    GitHub →
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
```

### Customizing Theme Colors

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#faf5ff',
          100: '#f3e8ff',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7e22ce',
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
};

export default config;
```

### Adding Analytics

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

## Deployment

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

Or connect your GitHub repository to Vercel for automatic deployments on every push to `main`.

### Environment Variables

```bash
# .env.local (not committed to git)
NEXT_PUBLIC_SITE_URL=https://your-domain.com
NEXT_PUBLIC_GA_ID=your-google-analytics-id
```

## Common Customization Patterns

### Add a Contact Form

```typescript
// components/Contact.tsx
'use client';
import { useState } from 'react';

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Integrate with your preferred email service
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    
    if (response.ok) {
      alert('Message sent successfully!');
      setFormData({ name: '', email: '', message: '' });
    }
  };

  return (
    <section className="py-20 px-4">
      <div className="max-w-2xl mx-auto">
        <h2 className="text-4xl font-bold text-center mb-12">Get In Touch</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            type="text"
            placeholder="Your Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="w-full px-4 py-3 bg-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            required
          />
          <input
            type="email"
            placeholder="Your Email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            className="w-full px-4 py-3 bg-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            required
          />
          <textarea
            placeholder="Your Message"
            value={formData.message}
            onChange={(e) => setFormData({ ...formData, message: e.target.value })}
            rows={5}
            className="w-full px-4 py-3 bg-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            required
          />
          <button
            type="submit"
            className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg font-semibold hover:opacity-90 transition-opacity"
          >
            Send Message
          </button>
        </form>
      </div>
    </section>
  );
}
```

### Smooth Scroll Navigation

```typescript
// components/Navigation.tsx
export default function Navigation() {
  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    element?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <nav className="fixed top-0 w-full bg-gray-900/80 backdrop-blur-sm z-50">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="text-xl font-bold">Portfolio</div>
        <div className="flex gap-6">
          <button onClick={() => scrollToSection('projects')} className="hover:text-purple-400">
            Projects
          </button>
          <button onClick={() => scrollToSection('experience')} className="hover:text-purple-400">
            Experience
          </button>
          <button onClick={() => scrollToSection('contact')} className="hover:text-purple-400">
            Contact
          </button>
        </div>
      </div>
    </nav>
  );
}
```

## Troubleshooting

### Images Not Loading
Ensure images are in the `public` directory and referenced with absolute paths:
```typescript
<img src="/projects/myproject.png" alt="Project" />
```

### Typing Animation Not Working
Check that the component is marked as `'use client'` for client-side interactivity:
```typescript
'use client';
import { useState, useEffect } from 'react';
```

### Tailwind Styles Not Applied
Verify `tailwind.config.ts` content paths include all component directories:
```typescript
content: [
  './app/**/*.{js,ts,jsx,tsx,mdx}',
  './components/**/*.{js,ts,jsx,tsx,mdx}',
],
```

### Build Errors
Clear Next.js cache and rebuild:
```bash
rm -rf .next
npm run build
```
