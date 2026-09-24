\version "2.26.0"

\include "drums-key.ily"

\header {
  title = "NT1.6"
  tagline = ##f
}

% one bar of the loop: hi-hat eighths, bass drum on 1 & 3, snare on 2 & 4
groove = \drummode {
  <bd hh>4 hh <sn hh> hh
}

fillA = \drummode {
  sn8 sn8 tomh4 tommh8 tommh8 toml4
}

fillB = \drummode {
  sn8 sn8 tomh4 tommh4 r4
}

line = \drummode { \repeat unfold 3 { \groove } }

\score {
  \new DrumStaff \with {
    drumStyleTable = #(alist->hash-table book-drums)
  } {
    \tempo 4 = 88
    \drummode {
      \ticFour \line \fillA \line \fillB
    }
  }
  \layout { }
  \midi { }
}
