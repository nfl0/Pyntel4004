/ Example program
        org     rom
fff,    =       9
        ldm     2
        inc     1
        ldm      fff
        jcn	6      fff
        fim     0p     180
        src     0p
lbl,    ldm     15
        wrm
        wr0
        wmp
        end