# Slide style

Each slide carries one message through a drawing, a figure, an annotated image or a worked example; its words are labels and short fragments. The speaker notes hold what is said, the footer holds the citation, and nothing on a slide talks about the slides themselves.

## The story

A talk tells one story, and each slide moves it one step. Choose the story before drawing anything:

| Talk | Story |
|---|---|
| A paper | The paper's own story: the problem and why it matters, why existing approaches fall short, the idea, the method step by step, the evidence, the limits |
| A method or a tutorial | One worked example, carried through every step of the method |
| A project or thesis update | The question, what was done, what was found, the decision it leads to |

- Make the problem concrete before the solution: show one case where it goes wrong, such as a failed segmentation or a misleading score, and return to the same case once the solution is in place.
- Build the solution step by step. Each step answers the question the previous one leaves open, and each idea appears before a slide relies on it.
- In a talk with several sections, give each section one guiding question, such as "Why do existing methods fail?" or "Does it generalise?". A divider shows the section number, an icon, the title and the question, and the outline slide lists the sections with their questions.
- A later slide may call back to an earlier one, for example by showing the earlier slide in grey under a stamp that names what it lacked.
- Let a thread run through the talk when the material has one, such as the opening failure case returning after each step of the method.
- Plan in a timed outline first: slide, start time, purpose. A content slide takes about a minute, a divider ten seconds.
- The last content slide answers the talk's opening question. The closing slide reuses the title layout for "Thank you", with discussion questions in its notes. An appendix holds backup slides (derivations, extra results, details likely to be asked) and the full references.

## One slide, one message

- When a slide makes two points, split it.
- Let the layout carry a contrast: the baseline beside the method, the input beside the output, a known concept beside the new one row for row, before against after.
- Titles are short noun phrases or the question the slide answers: "Outline", "Where the baseline fails", "How is the loss weighted?". A title gets no explanatory subtitle after a colon.
- Every slide keeps something concrete: a diagram, a figure, a labelled equation, an image, a table. A slide of sentences gets redrawn.
- Build a slide up in steps only for a twist, such as a red "But …" strip that appears on the second click.

## Pictures for kinds of content

| Content | Drawing |
|---|---|
| A problem | One concrete failure case, shown large, with the error marked |
| A model, a pipeline or an architecture | Blocks from left to right with what flows along each arrow (data, shapes, units); the block under discussion in colour, the rest in grey |
| An equation | The equation large and alone, each term labelled or coloured by its meaning; the derivation goes into the notes or the appendix |
| A loop or an iterative process | Boxes on a cycle with arrows, each step labelled with what it gives |
| Who or what does what, stage by stage | Swimlanes, one per actor or component, with the stages as columns |
| Results | One plot or table per message: the method in the accent colour, baselines in grey, the number that matters marked |
| Data | Example inputs beside their labels or outputs, at the same scale |
| A dense figure, micrograph or screenshot | The image with numbered red markers that also number the explanation beside it |
| Options or prior work to compare | Cards side by side with the same rows, each with a coloured head |
| Prior work across time | A row of cards along a timeline, each with its year and the idea it contributed |
| Two questions that decide a route | A 2 × 2 chart with the answers in its quadrants and examples placed as dots |
| Criteria that must all hold | Overlapping circles with the term in the shared middle |
| When things happen | A timeline with each item placed at its moment |
| A hierarchy | A tree with icons, guides and aligned notes; unchanged parts in grey, an arrow where one part splits into several |
| Paths that split and rejoin | A main line with branches that leave it and merge back, one label card per branch |
| A structure that recurs | The same drawing each time it returns, so that the audience recognises it, with the part under discussion highlighted |
| Code, files and commands | An editor window with the file's path in its tab; a terminal window (dark, three dots, green `$` prompts) for commands |
| A catch or a warning | A red strip with an icon along the bottom of the slide |
| A key statement | A box with an arrow from the thing it explains |
| Something new, explained by something known | An analogy drawn side by side, row for row |
| The title slide | An on-topic drawing or a simplified version of the key figure |

## Creative and informative

A creative element earns its place by carrying content:

- an analogy from the audience's own field, drawn row for row against the new idea;
- a recurring object that changes with the story, such as the failure case from the introduction shown again after each step of the method;
- an illustration that is itself the topic, such as the paper's own data or a simplified key figure in place of a stock photo;
- a drawing that replaces a slide of text, such as a method described in three paragraphs redrawn as a pipeline.

Images that do not match the topic, decorative photos and clip art stay out.

## Colour

Take the institution's palette and give each colour one meaning for the whole talk; every coloured element also carries a text label. The theme names its colours by these meanings; the RGB values are the template's defaults, to be replaced by the institution's.

| Colour in the theme | Default RGB | Meaning |
|---|---|---|
| `primary` (blue) | 31, 78, 121 | the subject: the method, the model or the tool; titles and structure |
| `accent` (red) | 190, 48, 60 | what to look at: a decision, a problem or a warning, numbered markers |
| `ink` (dark blue) | 24, 36, 51 | body text, and fixed inputs such as data and files |
| `good` (green) | 28, 128, 82 | what works: a passed check, an improved result |
| `grey`, `greymid`, `greylight`, `greypale` | 110, 145, 190 and 230 (each channel) | secondary text, baselines, unchanged parts, rules and guides |

Cards and panels use 8 % tints of these colours. Terminals are near black (12, 12, 12) with light grey text, green prompts and grey comments.

## Type and layout

- Pages are 16:9, 160 × 90 mm, with 8 mm side margins.
- Text is set in a clean sans (Latin Modern Sans), code in a monospace font with ligatures off (FiraCode Nerd Font Mono).
- Titles are 16.5 pt, bold and blue; body text 9 to 10 pt; labels 7 to 8 pt. Nothing the audience must read is smaller than 7 pt, code and equations included. When text does not fit, change the layout (columns, line breaks, a split) and keep the size.
- Content starts 4 mm below the title on every slide. The gap from a label to its content is always the same, and a larger, equal gap separates groups.
- Draw on a millimetre grid and fix the size of each picture, so that nothing shifts from slide to slide. Nothing overlaps: arrows stop short of text, and markers sit beside lines.
- A thin navigation bar at the top shows the sections with a dot per slide; the footer shows the group's logo at the left, then the citation, and the slide number alone at the right. Appendix slides are numbered A1, A2 and so on.
- Text inside a figure taken as an image, such as a plot from a paper or a screenshot, may be smaller than 7 pt; its numbered markers or its caption carry the message.

## Words on slides

- Write fragments and keep table cells short.
- Name the concept in plain words: "data leakage" rather than a description of how it happens.
- Leave qualifiers and provenance off the slide: "U-Net" rather than "a U-Net variant adapted from earlier work". The detail goes into the notes or the citation.
- Drop clauses that only add a name, such as "In the framework proposed by Smith et al., …" when the footer already cites it.
- Give each thing one name and keep it: once a unit is a "specimen", it is never also a "sample".
- Avoid bold lead-ins on list items and a summary box on every slide.

Habits that make text read as machine-written, and what to write instead:

| Instead of | Write |
|---|---|
| "not X, but Y" framing | the claim itself |
| groups of three by reflex | as many items as there are |
| powerful, seamless, robust, game-changing, leverage | a concrete word, or nothing |
| "Let's dive in", "In this section we will" | the content |
| a rhetorical question answered at once | the answer |
| a closing one-liner or moral | nothing |
| chains of dashes, emoji, bold everywhere | plain punctuation and one emphasis at most |

Slides, notes and README stay free of meta talk: nothing about earlier versions of the talk, how a slide was made or changed, or who asked for it, and no "now", "no longer" or "new" measured against an earlier draft. The history of a method belongs in a talk only when the history is the point. Material that will be published carries nothing internal to a group: no plans, unpublished work or internal data.

## Citations

- The footer carries citations only, in one form on every slide, two or three works at most, separated by " · ". No sentences and no badges. A footer that needs two lines breaks between works, never inside one.
- A work is cited by its authors, year and venue: "et al." for three or more authors and "and" for two; a journal by its abbreviation, volume and first page ("Author et al. (2026), Nat. Commun. 17, 11232"), a conference by its acronym ("Author et al. (2020), NeurIPS"), a preprint by its arXiv number, a book by its title in italics. The figure, equations or section used follow the venue.
- A figure taken from a paper carries that paper's citation on its slide, with the figure and its licence ("Fig. 2c (CC BY 4.0)"); a redrawn figure is cited with "after" and the figure it follows ("after Fig. 4f").
- The full references go on appendix slides, grouped by topic.
- A sources file records what each slide takes from where, how each figure or screenshot was made, so that it can be made again, and when each web page was read. A notices file lists third-party material with its licence.

## Speaker notes

- Every content slide has a note: the time range in bold first, such as `0:20–1:00`, then one sentence per line, so that a glance gives the next cue.
- The note carries what the slide leaves out: the explanation, the numbers, the caveats, and a definition of each term the audience may not know, such as an acronym or a word from a neighbouring field, where it first appears.
- A backup slide in the appendix starts its note with "If asked" and adds no time.
- A slide that builds up in steps attaches its note to the last step.
- Each note fits its page: its last words appear in the notes PDF.

## How the slides are made

1. Write the timed outline and choose the story.
2. Read the primary sources, such as the paper, its supplement, its code and its data, and record them.
3. Sketch each slide as a drawing, choosing its pattern from the table above, before writing any text.
4. Build in LaTeX Beamer with TikZ, in millimetre coordinates, one file per section. Use the source's real figures and data and real screenshots of real tools; redraw a figure when only part of it matters.
5. Render every page and look at the images, a contact sheet at a time, for spacing, overlaps, sizes and alignment.
6. Write the notes, rebuild, and check that every note fits.
7. On every build, check that there are no overfull boxes, that every note fits, that the outline's slide numbers match the footers, and that only the intended pages changed, by comparing the renders with the previous build.
8. Read every slide and note against the word rules and cut.

## Checklist for a slide

- [ ] One message, carried by a drawing, a figure or an example
- [ ] A title that is a short noun phrase or the question the slide answers
- [ ] Fragments only, and nothing to read below 7 pt
- [ ] Content 4 mm below the title, uniform gaps, nothing overlapping
- [ ] Colours used for their meaning, each element labelled
- [ ] Citations only in the footer
- [ ] A note with its time range, one sentence per line, new terms explained
- [ ] No meta talk, no machine-made phrasing, nothing internal

## Building blocks in Beamer

- Draw each figure inside the frame, in a `tikzpicture[x=1mm,y=1mm]` whose size `\useasboundingbox` fixes, rather than over the page, so that the notes thumbnail shows it too.
- Align columns with `[T]`, and add no `\vspace` at the start of a frame.
- A numbered marker is a filled red circle with a white bold digit, placed on the image and repeated as the label of the list item it numbers.
- A section divider is a blue box centred over a band of grey lines, holding the section number, an icon, the title and the guiding question.
- A speaker note reads `\note{\textbf{12:50--13:50}\par First point.\par Second point.}`.

The theme in `presentation/beamerthemetalk.sty` implements these colours, fonts and components, and the example talk in `presentation/slides/` uses each of them; the README lists the commands.
