# I-Fill-Forms Wireframes

## Screen 1: Landing & Upload State

```
┌─────────────────────────────────────────┐
│                                         │
│           I-Fill-Forms                  │
│     Conversation-Based Form Filler      │
│                                         │
│  ┌─────────────────────────────────────┐│
│  │                                     ││
│  │         📄 Upload PDFs              ││
│  │                                     ││
│  │    Drag & drop files here           ││
│  │         or click to browse          ││
│  │                                     ││
│  │     Supports: PDF files only        ││
│  │     Max size: 10MB per file         ││
│  │                                     ││
│  └─────────────────────────────────────┘│
│                                         │
│              [Browse Files]             │
│                                         │
│                   OR                    │
│                                         │
│         [Upload Multiple Files]         │
│                                         │
└─────────────────────────────────────────┘
```

## Screen 1a: Files Selected State

```
┌─────────────────────────────────────────┐
│           I-Fill-Forms                  │
│                                         │
│  ✅ Files Ready for Processing          │
│                                         │
│  📄 tax-form-2024.pdf        2.1 MB    │
│     Status: ✓ Valid PDF               │
│                                         │
│  📄 insurance-claim.pdf       1.8 MB    │
│     Status: ✓ Valid PDF               │
│                                         │
│  📄 application-form.pdf      950 KB    │
│     Status: ✓ Valid PDF               │
│                                         │
│  Total: 3 files (4.85 MB)             │
│                                         │
│              [Add More]                 │
│                                         │
│             [Continue] ─────────────────│
│                                         │
└─────────────────────────────────────────┘
```

## Screen 2: Audio Setup & Ready State

```
┌─────────────────────────────────────────┐
│           📋 3 Forms Ready              │
│                                         │
│  ┌─────────────────────────────────────┐│
│  │       🎤 Audio Setup                ││
│  │                                     ││
│  │   Microphone: ✅ Connected          ││
│  │   Status: Ready to listen           ││
│  │                                     ││
│  │        [🔊 Test Audio]              ││
│  │                                     ││
│  └─────────────────────────────────────┘│
│                                         │
│  ℹ️  How it works:                      │
│  • Start listening to capture speech    │
│  • Forms fill automatically as you speak│
│  • Watch live preview in real-time     │
│  • Review and export when done         │
│                                         │
│                                         │
│         [🎤 Start Listening] ───────────│
│                                         │
│              [← Back]                   │
│                                         │
└─────────────────────────────────────────┘
```

## Screen 3: Active Listening State

```
┌─────────────────────────────────────────┐
│  🔴 LISTENING...        [⏸ Pause] [⏹ Stop]│
│                                         │
│  📄 tax-form-2024.pdf          [Preview]│
│  ├─ Name: John Smith              ✅    │
│  ├─ SSN: ***-**-****             ✅    │
│  ├─ Address: 123 Main St...       ✅    │
│  └─ Income: $75,000               ⏳    │
│                                         │
│  📄 insurance-claim.pdf         [Preview]│
│  ├─ Name: John Smith              ✅    │
│  ├─ Policy #: [Empty]             ⌛    │
│  └─ Date of loss: [Empty]         ⌛    │
│                                         │
│  📄 application-form.pdf        [Preview]│
│  └─ Name: John Smith              ✅    │
│                                         │
│  ┌─────────────────────────────────────┐│
│  │ 🎵 Audio Activity                   ││
│  │ ████████████████░░░░░░░░░░░         ││
│  │                                     ││
│  │ Last captured:                      ││
│  │ "My annual income is seventy-five   ││
│  │  thousand dollars..."               ││
│  └─────────────────────────────────────┘│
│                                         │
└─────────────────────────────────────────┘
```

## Screen 3a: Field Detail Modal

```
┌─────────────────────────────────────────┐
│  🔴 LISTENING...        [⏸ Pause] [⏹ Stop]│
│                                         │
│  ┌─────────────────────────────────────┐│
│  │     Field Update Confirmation       ││
│  │                                     ││
│  │  Form: tax-form-2024.pdf            ││
│  │  Field: Annual Income               ││
│  │                                     ││
│  │  Heard: "seventy-five thousand"     ││
│  │  Value: $75,000                     ││
│  │  Confidence: 94% ✅                 ││
│  │                                     ││
│  │         [Accept] [Edit] [Skip]      ││
│  └─────────────────────────────────────┘│
│                                         │
│  [Background content dimmed]            │
│                                         │
└─────────────────────────────────────────┘
```

## Screen 4: Paused State

```
┌─────────────────────────────────────────┐
│  ⏸ PAUSED               [▶ Resume] [⏹ Stop]│
│                                         │
│  📊 Session Summary:                    │
│  • Duration: 3m 24s                     │
│  • Fields filled: 8 / 12               │
│  • Confidence: 91% average              │
│                                         │
│  📄 tax-form-2024.pdf          [Preview]│
│  ├─ Name: John Smith              ✅    │
│  ├─ SSN: ***-**-****             ✅    │
│  ├─ Address: 123 Main St...       ✅    │
│  ├─ Income: $75,000               ✅    │
│  └─ Filing Status: [Empty]         ⌛   │
│                                         │
│  📄 insurance-claim.pdf         [Preview]│
│  ├─ Name: John Smith              ✅    │
│  ├─ Policy #: ABC-123456          ✅    │
│  ├─ Date of loss: 03/15/2024      ✅    │
│  └─ Claim amount: [Empty]          ⌛   │
│                                         │
│  📄 application-form.pdf        [Preview]│
│  └─ Name: John Smith              ✅    │
│                                         │
└─────────────────────────────────────────┘
```

## Screen 5: Review & Verification State

```
┌─────────────────────────────────────────┐
│            📋 Review Forms              │
│                                         │
│  Session Complete: 12 fields filled    │
│  Total accuracy: 94%                    │
│                                         │
│  📄 tax-form-2024.pdf     [📱 Preview] │
│  ├─ ✅ Name: John Smith                 │
│  ├─ ✅ SSN: ***-**-****                │
│  ├─ ✅ Address: 123 Main St, City, ST   │
│  ├─ ✅ Income: $75,000                  │
│  └─ ⚠️  Filing Status: Single [Edit]    │
│                                         │
│  📄 insurance-claim.pdf   [📱 Preview] │
│  ├─ ✅ Name: John Smith                 │
│  ├─ ✅ Policy #: ABC-123456             │
│  ├─ ✅ Date of loss: 03/15/2024         │
│  └─ ⚠️  Claim amount: $2,500 [Edit]     │
│                                         │
│  📄 application-form.pdf  [📱 Preview] │
│  └─ ✅ Name: John Smith                 │
│                                         │
│  [📥 Export All]  [🔄 Start Over]      │
│                                         │
└─────────────────────────────────────────┘
```

## Screen 5a: Field Edit Modal

```
┌─────────────────────────────────────────┐
│            📋 Review Forms              │
│                                         │
│  ┌─────────────────────────────────────┐│
│  │           Edit Field                ││
│  │                                     ││
│  │  Form: tax-form-2024.pdf            ││
│  │  Field: Filing Status               ││
│  │                                     ││
│  │  Current: Single                    ││
│  │                                     ││
│  │  ┌─────────────────────────────────┐││
│  │  │ [v] Single                      │││
│  │  │     Married Filing Jointly      │││
│  │  │     Married Filing Separately   │││
│  │  │     Head of Household           │││
│  │  │     Qualifying Widow(er)        │││
│  │  └─────────────────────────────────┘││
│  │                                     ││
│  │         [Save] [Cancel]             ││
│  └─────────────────────────────────────┘│
│                                         │
└─────────────────────────────────────────┘
```

## Screen 6: Export Options

```
┌─────────────────────────────────────────┐
│           📤 Export Forms               │
│                                         │
│  Choose export format:                  │
│                                         │
│  ○ PDF (Filled forms)                   │
│  ○ PDF + JSON (Data backup)             │
│  ○ Individual files                     │
│  ● ZIP archive (All files) ✅           │
│                                         │
│  Files to include:                      │
│  ☑️ tax-form-2024.pdf                   │
│  ☑️ insurance-claim.pdf                 │
│  ☑️ application-form.pdf                │
│                                         │
│  Export location:                       │
│  📁 Downloads folder                    │
│                                         │
│                                         │
│       [📥 Download] [← Back]            │
│                                         │
└─────────────────────────────────────────┘
```

## Screen 7: Success & Complete

```
┌─────────────────────────────────────────┐
│              ✅ Complete!               │
│                                         │
│         Forms successfully filled       │
│             and downloaded              │
│                                         │
│  📊 Session Summary:                    │
│  • Files processed: 3                  │
│  • Fields filled: 12                   │
│  • Duration: 5m 47s                     │
│  • Average accuracy: 94%                │
│                                         │
│  📁 Files saved to:                     │
│     ~/Downloads/i-fill-forms-export.zip │
│                                         │
│                                         │
│      [🔄 Fill More Forms]               │
│                                         │
│            [🏠 Home]                    │
│                                         │
└─────────────────────────────────────────┘
```

## Mobile Wireframes

### Mobile: Upload Screen
```
┌─────────────────┐
│   I-Fill-Forms  │
├─────────────────┤
│                 │
│  ┌─────────────┐│
│  │             ││
│  │  📄 Upload  ││
│  │             ││
│  │ Tap to add  ││
│  │    files    ││
│  │             ││
│  └─────────────┘│
│                 │
│ [Browse Files]  │
│                 │
│    [Multiple]   │
│                 │
└─────────────────┘
```

### Mobile: Listening Screen
```
┌─────────────────┐
│ 🔴 LISTENING... │
├─────────────────┤
│                 │
│ 📄 tax-form.pdf │
│ • Name: ✅      │
│ • SSN: ✅       │
│ • Income: ⏳    │
│                 │
│ 📄 claim.pdf    │
│ • Name: ✅      │
│ • Policy: ⌛    │
│                 │
│ ┌─────────────┐ │
│ │🎵 ████████░░││ │
│ │"seventy..."  │ │
│ └─────────────┘ │
│                 │
│ [⏸ Pause] [⏹ Stop]│
│                 │
└─────────────────┘
```

### Mobile: Review Screen
```
┌─────────────────┐
│ 📋 Review (3)   │
├─────────────────┤
│                 │
│ 📄 tax-form.pdf │
│ ✅ 4/5 fields   │
│ ⚠️  1 needs edit │
│     [Preview]   │
│                 │
│ 📄 claim.pdf    │
│ ✅ 3/3 fields   │
│ ✓ Complete      │
│     [Preview]   │
│                 │
│ 📄 app-form.pdf │
│ ✅ 1/1 fields   │
│ ✓ Complete      │
│     [Preview]   │
│                 │
│   [Export All]  │
│                 │
└─────────────────┘
```

## Error State Wireframes

### Upload Error
```
┌─────────────────────────────────────────┐
│           I-Fill-Forms                  │
│                                         │
│  ❌ Upload Failed                       │
│                                         │
│  The following files couldn't be        │
│  uploaded:                              │
│                                         │
│  📄 document.doc                        │
│     ✗ Only PDF files are supported     │
│                                         │
│  📄 large-file.pdf                      │
│     ✗ File too large (15MB > 10MB)     │
│                                         │
│                                         │
│             [Try Again]                 │
│                                         │
│             [← Back]                    │
│                                         │
└─────────────────────────────────────────┘
```

### Audio Permission Error
```
┌─────────────────────────────────────────┐
│       🎤 Microphone Access              │
│                                         │
│  ❌ Permission Required                 │
│                                         │
│  I-Fill-Forms needs microphone access   │
│  to listen to your conversation and     │
│  fill forms automatically.              │
│                                         │
│  Please:                                │
│  1. Click the microphone icon in your  │
│     browser's address bar               │
│  2. Select "Allow"                      │
│  3. Refresh this page                   │
│                                         │
│                                         │
│           [Refresh Page]                │
│                                         │
│           [← Back]                      │
│                                         │
└─────────────────────────────────────────┘
```

## Component Specifications

### File Upload Zone
- **Size**: Full width, 200px height on desktop, 150px on mobile
- **Border**: 2px dashed gray, becomes blue on hover/drag
- **Typography**: 18px regular, gray text
- **Icon**: 48px document icon, centered

### Status Indicators
- **Success**: Green checkmark (✅) + "Completed"
- **Warning**: Orange exclamation (⚠️) + "Needs Review"
- **Processing**: Purple hourglass (⏳) + "Processing..."
- **Waiting**: Gray clock (⌛) + "Waiting"

### Audio Visualizer
- **Size**: Full width, 40px height
- **Bars**: 20 bars, 2px width, 4px spacing
- **Animation**: Real-time amplitude response
- **Colors**: Blue (#2563eb) for active bars

### Form Preview Cards
- **Padding**: 24px on desktop, 16px on mobile
- **Border**: 1px solid gray-200, 12px border radius
- **Shadow**: Subtle drop shadow on hover
- **Typography**: 16px regular for content, 14px for metadata

These wireframes prioritize clarity and simplicity while ensuring all key functionality is accessible and intuitive for users during the hackathon demo.