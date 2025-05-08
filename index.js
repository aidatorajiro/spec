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
let server = "api"

function XorShift(seed) {
    let [x, y, z, w] = seed;

    let t;

    t = x ^ (x << 11);
    x = y; y = z; z = w;
    w = (w ^ (w >>> 19)) ^ (t ^ (t >>> 8));

    return [x, y, z, w]
}

function pos_seed(pos) {
    return [415866776, 582600044, Math.floor(pos[0]*100), Math.floor(pos[1]*100)]; // todo
}

function choice(seed, arr) {
    let val = XorShift(seed)
    return [arr[Math.abs(val[3]) % arr.length], val]
}

var app = new Vue({
    el: '#app',
    data: {
      message: 'Hello Vue!',
      buildings: buildings,
      shortest_path: undefined,
      nearest_node: undefined,
      selected_building_name: undefined,
      selected_building_level: undefined,
      selected_building_pos: undefined
    },
    methods: {
        pos_to_pixpos: function (pos) {
            return [
                (pos[0] + vert_offset[0])*(dpi/one_inch_in_mm)*magnification,
                (pos[1] + vert_offset[1])*(dpi/one_inch_in_mm)*magnification
            ]
        },
        pixpos_to_pos: function (pixpos) {
            return [
                (pixpos[0]/magnification/(dpi/one_inch_in_mm)) - vert_offset[0],
                (pixpos[1]/magnification/(dpi/one_inch_in_mm)) - vert_offset[1]
            ]
        },
        get_shortest_path: async function (id_from, id_to) {
            this.shortest_path = (await (await fetch(server + "/get_shortest_path/" + id_from + "/" + id_to)).json()).result
        },
        get_nearest_node: async function (pos) {
            this.nearest_node = (await (await fetch(server + "/get_nearest_node/" + pos[0] + "/" + pos[1])).json()).result
        },
        query_building_name: function (pos, lev) {
            let lst = ["ア", "ディ", "ノッ", "パ", "せ", "すん", "メモ", "ダー", "ゲッ", "ギ", "ノ"]
            let lev_to_suffix = {
                "240": ["大学", "高校", "市役所", "タワー", "広場", "レストラン", "家電", "ステーション", "場", "束", "美術館", "ヒルズ", "センター", "病院", "局", "極", "クラブ", "銀行", "温泉"]
            }
            let suffix_t = {
                "大学": "University",
                "高校": "HighSchool",
                "市役所": "CityOffice",
                "タワー": "Tower",
                "広場": "Park",
                "レストラン": "Restaurant",
                "家電": "Electronics",
                "ステーション": "Station",
                "場": "Field",
                "束": "Fiber",
                "美術館": "Museum",
                "ヒルズ": "Hills",
                "センター": "Center",
                "病院": "Hospital",
                "局": "Department",
                "極": "Climax",
                "クラブ": "Club",
                "銀行": "Bank",
                "温泉": "HotSpring"
            }
            let s = ""
            let seed = pos_seed(pos)
            for (let i = 0; i < 10; i++) {
                [ret, seed] = choice(seed, lst)
                s += ret
            }
            [ret, seed] = choice(seed, lev_to_suffix[lev])
            s = s + ret + "/" + suffix_t[ret]
            return s
        },
        query_building_desc: function (lev) {
            if (lev == 240) {
                return "すごくそれらしい建物 Lv240"
            }
            if (lev == 200) {
                return "それらしい建物 Lv200"
            }
            if (lev == 150) {
                return "ちょっとした建物？ Lv150"
            }
        },
        query_building_rating: function () {
            // sigma 1, mu 3.25
        },
        async clickev(ev) {
            let pos = this.pixpos_to_pos([ev.pageX, ev.pageY])
            if (this.nearest_node === undefined) {
                console.log(pos)
                await this.get_nearest_node(pos)
            } else {
                let id_from = this.nearest_node[0]
                await this.get_nearest_node(pos)
                await this.get_shortest_path(id_from, this.nearest_node[0])
            }
        }
    }
})
