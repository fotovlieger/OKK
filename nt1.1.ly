\version "2.26.0"

\include "drums-key.ily"

measureOne = \drummode { hh4 hh4 <hh sn>4 hh4 }
measureTwo = \drummode { sn4 tomh4 tommh4 toml4 }
measureOneTwo = \drummode { \measureOne \measureTwo }
whole = \drummode { \repeat unfold 4 { \measureOneTwo } }

% printed score: no count-in
\score {
  \header {
    piece = "nt1.1"
    tagline = ##f
  }
  \new DrumStaff \with {
    drumStyleTable = #(alist->hash-table book-drums)
  } {
    \tempo 4 = 88
    \drummode {
      \whole
    }
  }
  \layout { }
}

% playback: stick-click count-in, then the music
\score {
  \new DrumStaff \with {
    drumStyleTable = #(alist->hash-table book-drums)
  } {
    \tempo 4 = 88
    \drummode {
      \ticFour
      \whole
    }
  }
  \midi { }
}
