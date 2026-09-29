\version "2.26.0"

\include "drums-key.ily"

measureOne = \drummode { <bd hh>4 hh4 hh4 hh4 }
measureTwo = \drummode { sn8 sn8 tomh4 tommh8 tommh8 toml4 }
measureOneTwo = \drummode { \measureOne \measureTwo }
whole = \drummode { \repeat unfold 4 { \measureOneTwo } }

% printed score: no count-in
\score {
  \header {
    piece = "nt1.3"
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
