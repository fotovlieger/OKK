\version "2.26.0"

\include "drums-key.ily"

grA = \drummode {
  <bd hh>4 hh <sn hh> hh
}
grB = \drummode {
  <bd hh>4 hh <sn hh> <sn hh>
}

fillA = \drummode {
  sn4 tomh8 tomh8 tommh4 toml4
}
fillB = \drummode {
  sn4 tomh8 tomh8 toml4 r4
}

lineA = \drummode { \grA \grB \grA \fillA }
lineB = \drummode { \grA \grA \grB \fillB }

% printed score: no count-in
\score {
  \header {
    piece = "NT1.7"
    tagline = ##f
  }
  \new DrumStaff \with {
    drumStyleTable = #(alist->hash-table book-drums)
  } {
    \tempo 4 = 88
    \drummode {
      \lineA \lineB
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
      \lineA \lineB
    }
  }
  \midi { }
}
