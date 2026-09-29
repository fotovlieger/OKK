\version "2.26.0"
\include "drums-key.ily"

\header {
  title = "Heavy Metal"
  subtitle = "E minor power chords + double bass"
  tagline = ##f
}

% ---------- drums: double-bass 16ths + backbeat + hi-hat 8ths ----------
drumPart = \drummode {
  \numericTimeSignature
  \time 4/4
  <<
    { \repeat unfold 8 { hh8 hh8 <sn hh>8 hh8 hh8 hh8 <sn hh>8 hh8 } }
    \\
    { \repeat unfold 8 {
        bd16 bd16 bd16 bd16 bd16 bd16 bd16 bd16
        bd16 bd16 bd16 bd16 bd16 bd16 bd16 bd16
      } }
  >>
}

% ---------- guitar: palm-muted power chords (E5 G5 A5 B5) ----------
guitar = {
  \clef "treble_8"          % standard guitar clef: written an octave higher than it sounds
  \numericTimeSignature
  \time 4/4
  \set Staff.midiInstrument = "distorted guitar"
  \repeat unfold 2 {
    \repeat unfold 8 { <e, b, e>8 }    % E5
    \repeat unfold 8 { <g, d g>8 }     % G5
    \repeat unfold 8 { <a, e a>8 }     % A5
    \repeat unfold 8 { <b, fis b>8 }   % B5
  }
}

% ---------- printed score: no count-in ----------
\score {
  \new StaffGroup <<
    \new DrumStaff \with {
      drumStyleTable = #(alist->hash-table book-drums)
    } { \tempo 4 = 88 \drumPart }
    \new Staff \with { instrumentName = "Guitar" } { \guitar }
  >>
  \layout { }
}

% ---------- playback: stick-click count-in, then the music ----------
\score {
  \new StaffGroup <<
    \new DrumStaff \with {
      drumStyleTable = #(alist->hash-table book-drums)
    } { \tempo 4 = 88 \ticFour \drumPart }
    \new Staff \with { instrumentName = "Guitar" } { R1 \guitar }
  >>
  \midi { }
}
