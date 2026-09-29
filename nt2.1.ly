\version "2.26.0"

\include "drums-key.ily"

\header {
  title = "Wzal Kotek na Plotek"
  subtitle = "Pools volksliedje - drumset (NT 2.1)"
  tagline = ##f
}

% one bar of the loop: hi-hat eighths, bass drum on 1 & 3, snare on 2 & 4
groove = \drummode {
  <bd hh>8 hh <sn hh> hh <bd hh> hh <sn hh> hh
}

% fill that ends phrases 1 and 2
fillA = \drummode {
  sn8 sn8 tomh4 tommh8 tommh8 toml4
}

% longer ending fill of phrase 3
fillB = \drummode {
  sn8 sn8 tomh4 tommh8 tommh8 toml4
  sn8 sn8 tommh8 tommh8 toml4 r4
}

phrase = \drummode {
  \repeat percent 3 { \groove }
  \fillA
}

music = \drummode {
  \phrase
  \phrase
  \repeat percent 3 { \groove }
  \fillB
  \bar "|."
}

% printed score: keeps the % repeat signs
\score {
  \new DrumStaff \with {
    drumStyleTable = #(alist->hash-table book-drums)
  } {
    \tempo 4 = 88
    \music
  }
  \layout { }
}

% playback: \unfoldRepeats expands the % signs into real notes for MIDI
\score {
  \new DrumStaff \with {
    drumStyleTable = #(alist->hash-table book-drums)
  } {
    \tempo 4 = 88
    \drummode {
      \ticFour
      \unfoldRepeats \music
    }
  }
  \midi { }
}
