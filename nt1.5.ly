\version "2.26.0"

\include "drums-key.ily"

\header {
  title = "nt1.5"
  tagline = ##f
}

measureOne = \drummode { <bd hh>4\f hh4\mp hh4 hh4 }
measureTwo = \drummode { sn4\mp tomh4\f tommh8 tommh8 toml8 toml8 }
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
