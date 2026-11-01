# 🎨 Design System Documentation

## Overview
This document describes the design system used in the AI-Powered Text-to-SQL Generator.

## Color Palette

### Primary Colors
- **Purple-Blue Gradient:** `#667eea → #764ba2`
- Used for: Headers, buttons, sidebar background, footer

### Background Colors
- **Page Background:** `#f5f7fa → #c3cfe2` (Light gradient)
- **Card Background:** White with transparency
- **Sidebar:** Purple gradient

### Semantic Colors
```css
Success: #84fab0 → #8fd3f4 (Green-blue gradient)
Warning: #ffeaa7 → #fdcb6e (Yellow-orange gradient)
Error:   #ff7675 → #d63031 (Red gradient)
Info:    #a8edea → #fed6e3 (Cyan-pink gradient)
```

### Code Display
- **SQL Box Background:** `#1e3c72 → #2a5298` (Dark blue gradient)
- **SQL Text Color:** `#00ff00` (Matrix green)

## Typography

### Font Families
```css
Primary: 'Poppins', sans-serif
  - Light (300): Subtitles
  - Regular (400): Body text
  - Semi-bold (600): Section headers
  - Bold (700): Main headers

Monospace: 'JetBrains Mono', monospace
  - Regular (400): SQL code
  - Medium (500): Technical text
```

### Font Sizes
```css
Main Header:     3.5rem (56px)
Sub Header:      1.3rem (20.8px)
Section Header:  1.8rem (28.8px)
Body:            1rem (16px)
Button:          1.1rem (17.6px)
Code:            0.95rem (15.2px)
```

## Components

### Buttons
```css
Style: Gradient background, white text
Border Radius: 50px (pill shape)
Padding: 0.75rem 2rem
Shadow: 0 8px 20px rgba(102, 126, 234, 0.4)
Hover: Transform translateY(-3px), enhanced shadow
Transition: 0.3s ease
```

### Input Fields
```css
Border: 2px solid #667eea
Border Radius: 15px
Padding: 1rem
Font Size: 1.1rem
Focus: Border #764ba2, shadow glow
```

### Cards
```css
Border Radius: 15-20px
Padding: 1.5-2rem
Box Shadow: 0 8-10px 20-30px with color tints
Background: Gradients based on type
```

### SQL Display Box
```css
Background: Dark blue gradient
Text Color: Matrix green (#00ff00)
Font: JetBrains Mono
Border Radius: 15px
Padding: 1.5rem
Shadow: 0 10px 30px rgba(0,0,0,0.3)
```

## Animations

### fadeInDown
```css
Duration: 1s
Easing: ease-in-out
From: opacity 0, translateY(-30px)
To: opacity 1, translateY(0)
Used for: Main header
```

### fadeInUp
```css
Duration: 1s
Easing: ease-in-out
From: opacity 0, translateY(30px)
To: opacity 1, translateY(0)
Used for: Subheader
```

### slideInLeft
```css
Duration: 0.5s
Easing: ease-out
From: opacity 0, translateX(-50px)
To: opacity 1, translateX(0)
Used for: SQL query box
```

### bounceIn
```css
Duration: 0.6s
Easing: ease-out
Keyframes: scale 0.3 → 1.05 → 1
Used for: Success messages
```

### Button Hover
```css
Duration: 0.3s
Easing: ease
Transform: translateY(-3px)
Shadow: Enhanced
```

## Layout

### Page Structure
```
┌─────────────────────────────────────┐
│           Header (gradient)         │
│         Feature Badges              │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────┐  ┌───────────────┐│
│  │  Sidebar    │  │  Main Content ││
│  │  (gradient) │  │               ││
│  │             │  │  Question     ││
│  │  Schema     │  │  Input        ││
│  │  Samples    │  │               ││
│  │  Examples   │  │  Results      ││
│  │  Stats      │  │  Display      ││
│  └─────────────┘  └───────────────┘│
│                                     │
├─────────────────────────────────────┤
│         Footer (gradient)           │
└─────────────────────────────────────┘
```

### Spacing System
```css
xs: 0.25rem (4px)
sm: 0.5rem (8px)
md: 1rem (16px)
lg: 1.5rem (24px)
xl: 2rem (32px)
2xl: 3rem (48px)
```

## Responsive Breakpoints

```css
Mobile: < 768px
Tablet: 768px - 1024px
Desktop: > 1024px
```

Streamlit handles most responsiveness automatically.

## Accessibility

### Contrast Ratios
- All text meets WCAG AA standards
- Minimum contrast ratio: 4.5:1 for normal text
- Minimum contrast ratio: 3:1 for large text

### Focus States
- All interactive elements have visible focus states
- Focus indicators use the primary purple color

### Font Sizes
- Minimum body text: 16px
- Headings scale appropriately
- All text is readable at 100% zoom

## Best Practices

1. **Consistent Spacing:** Use the spacing system
2. **Color Usage:** Stick to the defined palette
3. **Animation Duration:** Keep under 1 second
4. **Shadow Depth:** Use for hierarchy
5. **Border Radius:** Maintain consistency (15-20px)
6. **Font Weights:** Use appropriately for hierarchy
7. **Gradients:** Always use the defined gradients
8. **Hover States:** Always provide feedback

## File Reference

All styles are defined in `app.py` within the CSS markdown block.

To modify:
1. Locate the `st.markdown("""<style>...</style>""")` block
2. Update CSS as needed
3. Streamlit will auto-reload the changes

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Custom theme builder
- [ ] Additional color schemes
- [ ] More animation variants
- [ ] Advanced chart visualizations
- [ ] Responsive table improvements
