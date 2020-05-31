//画像の幅pixel: w

//96dot = 1inch = 25.4mm
//3.7795275590551185 dot = 1mm
//1dot = 0.26458333333333334mm

//pos to pixpos
//(pos + offset)*3.7795275590551185 = (pos + offset)*(dpi/one_inch_in_mm)

//post.png 10849 × 5388 96dpi
//lroc_color_poles_8k_orig.jpg 8192 × 4096 100dpi
//lroc_color_poles_8k.png 8137 × 4041 72 dpi

// 10849*(8192/8137) = 10922.331080250706 px

let one_inch_in_mm = 25.4
let dpi = 96
let vert_offset = [0, 1128.575]
let magnification = 1
let server = "http://localhost/"

var app = new Vue({
    el: '#app',
    data: {
      message: 'Hello Vue!',
      buildings: buildings
    },
    methods: {
        pos_to_pixpos: function (pos) {
            return [
                (pos[0] + vert_offset[0])*(dpi/one_inch_in_mm)*magnification,
                (pos[1] + vert_offset[1])*(dpi/one_inch_in_mm)*magnification
            ]
        },
        query_building_name: function () {
        },
        query_building_desc: function (lev) {
            if (lev == 240) {
                return "すごくそれらしい建物 Lv240"
            }
            if (lev == 200) {
                return "それらしい建物 Lv200"
            }
            if (lev == 150) {
                return "それらしい建物 Lv150"
            }
        },
        query_building_rating: function () {
            // sigma 1, mu 3.25
        }
    }
})
