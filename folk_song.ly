\version "2.26.0"
\include "drums-key.ily"

\header {
  title = "Folk Song"
  subtitle = "flute, banjo and percussion"
  tagline = ##f
}

% ---------- flute (melody, G major) ----------
flute = {
  \key g \major
  \numericTimeSignature
  \time 4/4
  \set Staff.midiInstrument = "flute"
  g'4 a' b' d'' | e''4 d'' b' g' | e''4 c'' a' g' | d''4 a' fis' a' |
  g'4 a' b' d'' | e''4 d'' b' g' | a'4 fis' a' b'  | g'2. r4
}

% ---------- banjo (fast 16th-note rolls on G Em C D) ----------
rollG  = { \repeat unfold 4 { g'16 b'16 d''16 b'16 } }
rollEm = { \repeat unfold 4 { e'16 g'16 b'16 g'16 } }
rollC  = { \repeat unfold 4 { c'16 e'16 g'16 e'16 } }
rollD  = { \repeat unfold 4 { d'16 fis'16 a'16 fis'16 } }

banjo = {
  \key g \major
  \numericTimeSignature
  \time 4/4
  \set Staff.midiInstrument = "banjo"
  \rollG \rollEm \rollC \rollD
  \rollG \rollEm \rollC \rollD
}

% ---------- percussion (kick / side stick / tambourine, with variation) ----------
groove = \drummode { <bd tamb>8 tamb8 <ss tamb>8 tamb8 <bd tamb>8 tamb8 <ss tamb>8 tamb8 }
drive  = \drummode { <bd tamb>8 tamb8 <ss tamb>8 bd8 <bd tamb>8 tamb8 <ss tamb>8 tamb8 }
accent = \drummode { <bd tamb>8 tamb8 <ss tamb>8 tamb8 <bd hho tamb>8 tamb8 <ss tamb>8 tamb8 }
fillA  = \drummode { ss8 ss8 toml8 toml8 ss8 ss8 <ss tamb>4 }
fillB  = \drummode { toml8 toml8 tommh8 tommh8 tomh8 tomh8 <ss bd>4 }

perc = \drummode {
  \numericTimeSignature
  \time 4/4
  \groove \groove \accent \fillA
  \groove \drive  \accent \fillB
}

% ---------- printed score: no count-in ----------
\score {
  \new StaffGroup <<
    \new Staff \with { instrumentName = "Flute" } { \flute }
    \new Staff \with { instrumentName = "Banjo" } { \banjo }
    \new DrumStaff \with {
      instrumentName = "Percussion"
      drumStyleTable = #(alist->hash-table book-drums)
    } { \tempo 4 = 88 \perc }
  >>
  \layout { }
}

% ---------- playback: stick-click count-in, then the music ----------
\score {
  \new StaffGroup <<
    \new Staff \with { instrumentName = "Flute" } { R1 \flute }
    \new Staff \with { instrumentName = "Banjo" } { R1 \banjo }
    \new DrumStaff \with {
      instrumentName = "Percussion"
      drumStyleTable = #(alist->hash-table book-drums)
    } { \tempo 4 = 88 \ticFour \perc }
  >>
  \midi { }
}
