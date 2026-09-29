\version "2.26.0"

\header {
  tagline = ##f
}

% Combined handout: all nt1.* exercises stacked, printed from one file.
% Each included file defines its music and emits a layout score plus a
% MIDI score; the layout scores are collected into this single PDF.
\paper {
  paper-width = 297\mm
  paper-height = 210\mm
  top-margin = 0\mm
  bottom-margin = 0\mm
  left-margin = 0\mm
  right-margin = 0\mm
  indent = 0\mm
  ragged-right = ##f
  markup-markup-spacing.basic-distance = #2
  markup-system-spacing.basic-distance = #5
  score-markup-spacing.basic-distance = #2
  score-system-spacing.basic-distance = #8
  system-system-spacing.basic-distance = #8
  system-system-spacing.minimum-distance = #5
  ragged-last-bottom = ##f
}

\include "nt1.1.ly"
\include "nt1.2.ly"
\include "nt1.3.ly"
\include "nt1.4.ly"
\include "nt1.5.ly"
\include "nt1.6.ly"
\include "nt1.7.ly"
