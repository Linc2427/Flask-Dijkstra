import networkx as nx
from geopy.distance import geodesic
from flask import Flask, render_template, url_for, request
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra

# Data node dengan latitude dan longitude
nodes = {
    'Jl. Gebang Lor': (-7.280069443224376, 112.78974571816937),
    'Jl. Gebang Lor': (-7.280145566750169, 112.78961497638991),
    'Jl. Gebang Lor': (-7.2802087556657105, 112.78950299416502),
    'Jl. Gebang Lor': (-7.2802699491333165, 112.78937894199969),
    'Jl. Gebang Lor': (-7.280336463765849, 112.78927098308586),
    'Jl. Gebang Lor': (-7.280397333936039, 112.78912039964773),
    'Jl. Gebang Lor': (-7.28046617655809, 112.78901411711398),
    'Jl. Gebang Lor': (-7.280549319808272, 112.78886324285753),
    'Jl. Gebang Lor': (-7.280612508666919, 112.78875461339429),
    'Jl. Gebang Lor': (-7.28067968839108, 112.78864598393105),
    'Jl. Gebang Lor': (-7.280718931990859, 112.78852126120742),
    'Jl. Gebang Lor': (-7.280759505875241, 112.78839117407244),
    'Jl. Gebang Lor': (-7.280825355287955, 112.78826108693491),
    'Jl. Gebang Lor': (-7.280868589746492, 112.7881296586918),
    'Jl. Gebang Lor': (-7.280933108850875, 112.78802639364649),
    'Jl. Gebang Lor': (-7.280994967364921, 112.78789630651151),
    'Jl. Gebang Lor': (-7.281061481888018, 112.78776957213464),
    'Jl. Gebang Lor': (-7.281125335819579, 112.78766027211915),
    'Jl. Gebang Lor': (-7.281189189747121, 112.78753554939448),
    'Jl. Gebang Lor': (-7.281272998006556, 112.78742356717001),
    'Jl. Gebang Lor': (-7.281317562709571, 112.78729683279623),
    'Jl. Gebang Lor': (-7.281399375514888, 112.78716808675921),
    'Jl. Gebang Lor': (-7.281441279626928, 112.7870614689527),
    'Jl. Gebang Lor': (-7.281507128937941, 112.78693138181768),
    'Jl. Gebang Lor': (-7.2815477027533175, 112.78680330633324),
    'Jl. Gebang Lor': (-7.281591602284642, 112.78667388975049),
    'Jl. Gebang Lor': (-7.281634171524302, 112.78654514371715),
    'Jl. Gebang Lor': (-7.281678736191414, 112.78641505658214),
    'Jl. Gebang Lor': (-7.281720640279079, 112.78628765165132),
    'Jl. Gebang Lor': (-7.281761879216973, 112.78615823506857),
    'Jl. Gebang Lor': (-7.281804448439204, 112.78602948903807),
    'Jl. Gebang Lor': (-7.281847017658242, 112.78590141355451),
    'Jl. Gebang Lor': (-7.281849013090248, 112.78579345464351),

    'Jl. Gebang Putih': (-7.281846506181156, 112.78579243258743),
    'Jl. Gebang Putih': (-7.28199682870072, 112.78578170375151),
    'Jl. Gebang Putih': (-7.282126531721749, 112.78574884669104),
    'Jl. Gebang Putih': (-7.282250248415934, 112.78572873012288),
    'Jl. Gebang Putih': (-7.2824025662296705, 112.78570995465999),
    'Jl. Gebang Putih': (-7.282530273703914, 112.78568782643546),
    'Jl. Gebang Putih': (-7.282656650858595, 112.78564424053828),
    'Jl. Gebang Putih': (-7.282783693117638, 112.78560266629856),
    'Jl. Gebang Putih': (-7.282912065625561, 112.7855791969696),
    'Jl. Gebang Putih': (-7.283040438096907, 112.78553561107304),
    'Jl. Gebang Putih': (-7.283166149963641, 112.78551616505757),
    'Jl. Gebang Putih': (-7.2832965177876705, 112.7854940368331),

    'Gg. Puskesmas': (-7.2832759658201125, 112.7855154660366),
    'Gg. Puskesmas': (-7.2832767593552115, 112.78564266422099),
    'Gg. Puskesmas': (-7.283294217099462, 112.78579546203757),
    'Gg. Puskesmas': (-7.283317229581525, 112.78592346021266),
    'Gg. Puskesmas': (-7.283337861458853, 112.7860546583395),
    'Gg. Puskesmas': (-7.283337861458509, 112.78605225837222),
    'Gg. Puskesmas': (-7.283356112734093, 112.78618905641744),
    'Gg. Puskesmas': (-7.2833767446099325, 112.78633305435974),
    'Gg. Puskesmas': (-7.283397376486267, 112.78646105253982),
    'Gg. Puskesmas': (-7.283402931221651, 112.78659065068791),
    'Gg. Puskesmas': (-7.2834195954274055, 112.78671864885887),
    'Gg. Puskesmas': (-7.283442607900983, 112.7868674467326),
    'Gg. Puskesmas': (-7.283443401434528, 112.78699464491498),
    'Gg. Puskesmas': (-7.283463239772841, 112.78712424306306),
    'Gg. Puskesmas': (-7.283464033306782, 112.78727704088385),
    'Gg. Puskesmas': (-7.283442607901402, 112.78740423906623),
    'Gg. Puskesmas': (-7.283444988502475, 112.78753143725656),
    'Gg. Puskesmas': (-7.28346323977368, 112.78766423535892),
    'Gg. Puskesmas': (-7.2835108517820375, 112.78779223352987),
    'Gg. Puskesmas': (-7.283593379251237, 112.78804502991751),
    'Gg. Puskesmas': (-7.283614804651349, 112.78819702775112),
    'Gg. Puskesmas': (-7.283637817114913, 112.78832502592208),
    'Gg. Puskesmas': (-7.283678287306584, 112.78845542405874),
    'Gg. Puskesmas': (-7.283698125634502, 112.78858662218397),
    'Gg. Puskesmas': (-7.283720344561048, 112.78873302009634),

    'Gg. Gebang Kidul Sepuhan': (-7.2836991963499145, 112.78875769158556),
    'Gg. Gebang Kidul Sepuhan': (-7.283572154352262, 112.78875232716759),
    'Gg. Gebang Kidul Sepuhan': (-7.283423827784612, 112.78878049036192),
    'Gg. Gebang Kidul Sepuhan': (-7.2833579787513125, 112.78866917868824),
    'Gg. Gebang Kidul Sepuhan': (-7.283209652111731, 112.78864772101561),
    'Gg. Gebang Kidul Sepuhan': (-7.28308327511543, 112.78866984924004),
    'Gg. Gebang Kidul Sepuhan': (-7.282973526644187, 112.78869264801638),

    'Gg. Puskesmas Kedai Mamira': (-7.282721109964167, 112.78805062810113),
    'Gg. Puskesmas Kedai Mamira': (-7.282874715598693, 112.78800508253629),
    'Gg. Puskesmas Kedai Mamira': (-7.282994437606946, 112.78798344839251),
    'Gg. Puskesmas Kedai Mamira': (-7.283129971910463, 112.78795953697096),
    'Gg. Puskesmas Kedai Mamira': (-7.283253082204329, 112.78796409152729),
    'Gg. Puskesmas Kedai Mamira': (-7.283406687656596, 112.78796067560991),
    'Gg. Puskesmas Kedai Mamira': (-7.28352640951778, 112.78793904146653),

    'Gg. Puskesmas Warkop Salawat': (-7.282722151780604, 112.78772796623365),
    'Gg. Puskesmas Warkop Salawat': (-7.282848528878746, 112.78772729568169),
    'Gg. Puskesmas Warkop Salawat': (-7.282995525353606, 112.7877071791142),
    'Gg. Puskesmas Warkop Salawat': (-7.283123897800933, 112.78770449690508),
    'Gg. Puskesmas Warkop Salawat': (-7.283254930779897, 112.78770181469625),
    'Gg. Puskesmas Warkop Salawat': (-7.283403922545356, 112.7876830392333),
    'Gg. Puskesmas Warkop Salawat': (-7.283443831045141, 112.78766292266594),

    'Jl. Gebang Kidul': (-7.282508175800044, 112.78570789016038),
    'Jl. Gebang Kidul': (-7.282528130090248, 112.78583864784824),
    'Jl. Gebang Kidul': (-7.282548084379572, 112.78598751044673),
    'Jl. Gebang Kidul': (-7.282550079808448, 112.78611558592563),
    'Jl. Gebang Kidul': (-7.282573359811432, 112.78624366140451),
    'Jl. Gebang Kidul': (-7.282571364383039, 112.78639319456296),
    'Jl. Gebang Kidul': (-7.282592648956229, 112.78652328169858),
    'Jl. Gebang Kidul': (-7.282614598671277, 112.78665470993869),
    'Jl. Gebang Kidul': (-7.282636548385254, 112.78680290198493),
    'Jl. Gebang Kidul': (-7.2826152638141375, 112.78693030691157),
    'Jl. Gebang Kidul': (-7.282633745841481, 112.78705957359202),
    'Jl. Gebang Kidul': (-7.282678310409232, 112.78746861046176),
    'Jl. Gebang Kidul': (-7.282676980123701, 112.78759869759736),
    'Jl. Gebang Kidul': (-7.282700260120488, 112.78774487799312),
    'Jl. Gebang Kidul': (-7.282700925263236, 112.78787563568099),
    'Jl. Gebang Kidul': (-7.282696269264059, 112.78800371115987),
    'Jl. Gebang Kidul': (-7.2826995949789755, 112.78815391487001),
    'Jl. Gebang Kidul': (-7.282719549260667, 112.78828199034889),
    'Jl. Gebang Kidul': (-7.282781407528259, 112.78839061981266),
    'Jl. Gebang Kidul': (-7.282845261214893, 112.78852137750053),
    'Jl. Gebang Kidul': (-7.282934390303934, 112.78862531309856),
    'Jl. Gebang Kidul': (-7.282977624560124, 112.78875271802944),
    'Jl. Gebang Kidul': (-7.282954344578132, 112.78888615792629),

    'Jl. Gebang Wetan': (-7.280676422151531, 112.78864689201023),
    'Jl. Gebang Wetan': (-7.280830372912687, 112.78866801419625),
    'Jl. Gebang Wetan': (-7.280951529390553, 112.78869097309254),
    'Jl. Gebang Wetan': (-7.281079062488126, 112.78871576870114),
    'Jl. Gebang Wetan': (-7.281378688600479, 112.78870934021002),
    'Jl. Gebang Wetan': (-7.28135787372911, 112.78873319490141),
    'Jl. Gebang Wetan': (-7.281482920920575, 112.78879622681244),
    'Jl. Gebang Wetan': (-7.281613289231981, 112.78883914215612),
    'Jl. Gebang Wetan': (-7.281743657510536, 112.78886328203824),
    'Jl. Gebang Wetan': (-7.281870034882335, 112.78888541026232),
    'Jl. Gebang Wetan': (-7.281995081936119, 112.78892966671103),
    'Jl. Gebang Wetan': (-7.282123454667864, 112.78895045383061),
    'Jl. Gebang Wetan': (-7.282272446812382, 112.78897124095067),
    'Jl. Gebang Wetan': (-7.282400819467883, 112.78897392316014),
    'Jl. Gebang Wetan': (-7.282532517800604, 112.78896922929438),
    'Jl. Gebang Wetan': (-7.28267751895077, 112.78895045383156),
    'Jl. Gebang Wetan': (-7.282805891489659, 112.78894710107015),
    'Jl. Gebang Wetan': (-7.282932268564125, 112.78890686793514),
    'Jl. Gebang Wetan': (-7.282996787373136, 112.7888673053519),

    'Jl. Gebang Wetan Gg. I': (-7.281378688600479, 112.78871250328166),
    'Jl. Gebang Wetan Gg. I': (-7.281422588148342, 112.78858040448938),
    'Jl. Gebang Wetan Gg. I': (-7.281420592715483, 112.78845635232067),
    'Jl. Gebang Wetan Gg. I': (-7.281466487691663, 112.78832894739496),
    'Jl. Gebang Wetan Gg. I': (-7.28148311630691, 112.78819818970403),
    'Jl. Gebang Wetan Gg. I': (-7.2815077266543025, 112.78804932710564),

    'Jl. Rodah': (-7.281252775397267, 112.78749286809372),
    'Jl. Rodah': (-7.281382478632589, 112.78750963190008),
    'Jl. Rodah': (-7.281528145299103, 112.78753243067733),
    'Jl. Rodah': (-7.281656518168756, 112.78755254724548),
    'Jl. Rodah': (-7.28178156527693, 112.78755455890222),
    'Jl. Rodah': (-7.281933218108881, 112.78757534602163),
    'Jl. Rodah': (-7.282060925714647, 112.78760149755918),
    'Jl. Rodah': (-7.282187968144333, 112.78762094357508),
    'Jl. Rodah': (-7.282315010537545, 112.7876370368296),
    'Jl. Rodah': (-7.282462672327679, 112.78765916505368),
    'Jl. Rodah': (-7.2825950357878675, 112.78767995217402),
    'Jl. Rodah': (-7.282676848356234, 112.78768464603972),

    'Jl. Rodah Sekolahan': (-7.2818967950183655, 112.78759480148886),
    'Jl. Rodah Sekolahan': (-7.281890168033269, 112.78774750707467),
    'Jl. Rodah Sekolahan': (-7.281893008169696, 112.78787921564924),
    'Jl. Rodah Sekolahan': (-7.281888274609004, 112.78802428595785),
    'Jl. Rodah Sekolahan': (-7.281885434472487, 112.78815790334544),
    'Jl. Rodah Sekolahan': (-7.28191478254958, 112.78828483986689),
    'Jl. Rodah Sekolahan': (-7.281953597745144, 112.78841368520686),
    'Jl. Rodah Sekolahan': (-7.281974425409773, 112.78853680408709),
    'Jl. Rodah Sekolahan': (-7.281971585274146, 112.78869141849425),
    'Jl. Rodah Sekolahan': (-7.281967798425821, 112.788819309424),
    'Jl. Rodah Sekolahan': (-7.2819526510335395, 112.78888516370789),

    'Gg. Mawar': (-7.282251333036491, 112.78761685937461),
    'Gg. Mawar': (-7.282246677032646, 112.7874679967762),
    'Gg. Mawar': (-7.282229383303659, 112.78733858019294),
    'Gg. Mawar': (-7.282211424429877, 112.78721050471019),
    'Gg. Mawar': (-7.282184153547093, 112.78706432432077),
    'Gg. Mawar': (-7.282168190102291, 112.78693289607747),
    'Gg. Mawar': (-7.282168190102291, 112.78680549115093),
    'Gg. Mawar': (-7.282148900938982, 112.78665461689148),
    'Gg. Mawar': (-7.282147570651861, 112.78652452975595),
    'Gg. Mawar': (-7.28212628605755, 112.78643869906863),

    'Gg. Mawar Joder Lama': (-7.281530054940518, 112.78692997733002),
    'Gg. Mawar Joder Lama': (-7.281676386703356, 112.7869145546282),
    'Gg. Mawar Joder Lama': (-7.281804094385163, 112.78691187241951),
    'Gg. Mawar Joder Lama': (-7.281933132315453, 112.78690919021054),
    'Gg. Mawar Joder Lama': (-7.282082789664204, 112.78691053131479),
    'Gg. Mawar Joder Lama': (-7.282166597756622, 112.78690919021032),

    'Jl. Kanoman II (dalam)': (-7.281700452143313, 112.7888837601504),
    'Jl. Kanoman II (dalam)': (-7.281697791566422, 112.78903597551),
    'Jl. Kanoman II (dalam)': (-7.281698456710301, 112.7891613687833),
    'Jl. Kanoman II (dalam)': (-7.281698456710161, 112.78942221360921),
    'Jl. Kanoman II (dalam)': (-7.281697791565645, 112.78956772344846),
    'Jl. Kanoman II (dalam)': (-7.281696461277201, 112.78969982224073),

    'Jl. Kanoman II (luar)': (-7.280121518544595, 112.78970052533187),
    'Jl. Kanoman II (luar)': (-7.28024989181267, 112.78969717257064),
    'Jl. Kanoman II (luar)': (-7.280404205747919, 112.78969851367528),
    'Jl. Kanoman II (luar)': (-7.280530583497209, 112.7897239946606),
    'Jl. Kanoman II (luar)': (-7.2806775807338004, 112.78972332410856),
    'Jl. Kanoman II (luar)': (-7.280805288697162, 112.78971997134735),
    'Jl. Kanoman II (luar)': (-7.28092900575734, 112.7897213124514),
    'Jl. Kanoman II (luar)': (-7.281083319455306, 112.7897213124514),
    'Jl. Kanoman II (luar)': (-7.281207701583221, 112.78972198300367),
    'Jl. Kanoman II (luar)': (-7.281338069974649, 112.7897193007947),
    'Jl. Kanoman II (luar)': (-7.281463117176406, 112.78972332410842),
    'Jl. Kanoman II (luar)': (-7.281616765546238, 112.78971930079497),
    'Jl. Kanoman II (luar)': (-7.281699908583514, 112.78970387809343)
}

def nearest_location(G, current_pos):
    nearest_node = None
    shortest_distance = float('inf') # Inisialisasi dengan nilai tak terhingga

    # Hitung jarak dari posisi saat ini ke setiap node dan temukan node terdekat
    for node_id, node_attrs in G.nodes(data=True):
        node_pos = node_attrs['pos']
        distance = geodesic(current_pos, node_pos).kilometers
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_node = node_id

    return nearest_node

G = nx.Graph()

# Tambahkan node ke graf
for node_id, (lat, lon) in nodes.items():
    G.add_node(node_id, pos=(lat, lon))

# Hitung jarak antara setiap pasangan node dan tambahkan edge
for node_id1, (lat1, lon1) in nodes.items():
    for node_id2, (lat2, lon2) in nodes.items():
        if node_id1 != node_id2:
            distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
            G.add_edge(node_id1, node_id2, weight=distance)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cur_lat = float(request.form['cur-lat'])
        cur_long = float(request.form['cur-long'])
        veh_lat = float(request.form['veh-lat'])
        veh_long = float(request.form['veh-long'])

        current_pos = (cur_lat, cur_long)
        nearest_node = nearest_location(G, current_pos)
        
        vehicle_node = nearest_location(G, (veh_lat, veh_long))
        
        # shortest_path = nx.dijkstra_path(G, source=nearest_node, target=target_node, weight='weight')
        shortest_path = nx.dijkstra_path(G,
        source=nearest_node, target=vehicle_node, weight='weight')

        return render_template('home.html', shortest_path=shortest_path)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
