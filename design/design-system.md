# I-Fill-Forms Design System

## Color Palette

### Primary Colors
```css
:root {
  --primary: #2563eb;      /* Blue - action buttons */
  --primary-light: #3b82f6;
  --primary-dark: #1d4ed8;
}
```

### Status Colors
```css
:root {
  --success: #059669;      /* Green - completed fields */
  --warning: #d97706;      /* Orange - needs review */
  --error: #dc2626;        /* Red - errors */
  --processing: #7c3aed;   /* Purple - in progress */
}
```

### Neutral Colors
```css
:root {
  --gray-50: #f8fafc;
  --gray-100: #f1f5f9;
  --gray-200: #e2e8f0;
  --gray-300: #cbd5e1;
  --gray-400: #94a3b8;
  --gray-500: #64748b;
  --gray-600: #475569;
  --gray-700: #334155;
  --gray-800: #1e293b;
  --gray-900: #0f172a;
  
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-accent: #f1f5f9;
}
```

## Typography

### Font Families
```css
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'SF Mono', Monaco, 'Cascadia Code', monospace;
}
```

### Font Sizes
```css
:root {
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
}
```

### Font Weights
```css
:root {
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

## Spacing System

### Base Units (4px system)
```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
}
```

### Border Radius
```css
:root {
  --radius-sm: 0.25rem;  /* 4px */
  --radius: 0.5rem;      /* 8px */
  --radius-lg: 0.75rem;  /* 12px */
  --radius-xl: 1rem;     /* 16px */
}
```

## Component Styles

### Buttons
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius);
  font-weight: var(--font-medium);
  font-size: var(--text-base);
  font-family: var(--font-sans);
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
  text-decoration: none;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
}

.btn-secondary {
  background-color: var(--gray-100);
  color: var(--gray-700);
  border: 1px solid var(--gray-200);
}

.btn-secondary:hover {
  background-color: var(--gray-200);
}

.btn-lg {
  padding: var(--space-4) var(--space-8);
  font-size: var(--text-lg);
}

.btn-full {
  width: 100%;
}
```

### Cards & Containers
```css
.card {
  background: var(--bg-primary);
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--space-4);
}

.container-sm {
  max-width: 600px;
  margin: 0 auto;
  padding: var(--space-4);
}
```

### Status Indicators
```css
.status {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

.status-success {
  background: #dcfdf7;
  color: var(--success);
}

.status-warning {
  background: #fef3c7;
  color: var(--warning);
}

.status-error {
  background: #fef2f2;
  color: var(--error);
}

.status-processing {
  background: #f3e8ff;
  color: var(--processing);
}

.status-processing::before {
  content: '⏳';
  margin-right: var(--space-1);
}
```

### Form Elements
```css
.upload-zone {
  border: 2px dashed var(--gray-300);
  border-radius: var(--radius-lg);
  padding: var(--space-12);
  text-align: center;
  background: var(--bg-accent);
  transition: all 0.15s ease;
  cursor: pointer;
}

.upload-zone:hover,
.upload-zone.drag-over {
  border-color: var(--primary);
  background: #eff6ff;
}

.file-list {
  list-style: none;
  padding: 0;
  margin: var(--space-4) 0;
}

.file-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--bg-primary);
  border: 1px solid var(--gray-200);
  border-radius: var(--radius);
  margin-bottom: var(--space-2);
}

.file-item:last-child {
  margin-bottom: 0;
}
```

### Progress & Loading
```css
.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--gray-200);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--primary);
  transition: width 0.3s ease;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid var(--gray-200);
  border-top: 2px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

## Mobile Responsiveness

```css
@media (max-width: 768px) {
  .container {
    padding: var(--space-2);
  }
  
  .btn-lg {
    width: 100%;
    padding: var(--space-4);
  }
  
  .card {
    padding: var(--space-4);
  }
  
  .upload-zone {
    padding: var(--space-8);
  }
  
  .file-item {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .container {
    padding: var(--space-2);
  }
  
  .text-3xl {
    font-size: var(--text-2xl);
  }
  
  .text-2xl {
    font-size: var(--text-xl);
  }
}
```

## Accessibility

### Focus States
```css
*:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

.btn:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```

### High Contrast Support
```css
@media (prefers-contrast: high) {
  :root {
    --gray-300: #000000;
    --gray-200: #333333;
  }
  
  .card {
    border: 2px solid var(--gray-800);
  }
}
```

## Usage Guidelines

### Do's
- Use consistent spacing from the spacing system
- Stick to the defined color palette
- Use semantic color meanings (green for success, red for error)
- Keep components simple and functional
- Test on mobile devices

### Don'ts  
- Don't create custom colors outside the palette
- Don't use complex animations (keep it simple for hackathon)
- Don't mix different border radius values
- Don't use custom fonts (stick to system fonts for performance)

## Implementation Notes

- All CSS custom properties should be defined in your root stylesheet
- Use semantic HTML elements for accessibility
- Implement focus management for keyboard navigation
- Test with screen readers if possible
- Keep bundle size minimal for fast loading