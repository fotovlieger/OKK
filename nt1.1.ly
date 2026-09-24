\version "2.26.0"

\include "drums-key.ily"

\header {
  title = "nt1.1"
  tagline = ##f
}

measureOne = \drummode { hh4\f hh4 <hh sn>4\mf hh4\f }
measureTwo = \drummode { sn4 tomh4 tommh4 toml4 }
measureOneTwo = \drummode { \measureOne \measureTwo }
whole = \drummode { \tics \repeat unfold 4 { \measureOneTwo } }

\score {
  \new DrumStaff \with {
    drumStyleTable = #(alist->hash-table book-drums)
  } {
    \tempo 4 = 120
    \drummode {
      \whole
    }
  }
  \layout { }
  \midi { }
}
