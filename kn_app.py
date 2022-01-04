import json
from flask import Flask, jsonify, request
import json2html
import json2table
from kn.kn_scrapper import KNScrapper
from kn.kn_compare import KnTransfers
from datetime import datetime
from contextlib import redirect_stdout
import io
from kn.config import KnConfig
from kn.db_managment import DbManagment
BASE_URL = 'http://localhost:5000'
cfg = KnConfig()
kn_app = Flask(__name__)

@kn_app.route('/')
@kn_app.route('/test')
def index():
    urls_list = [f"<a href={cfg.base_url}/block/A03/scrap>Scrap A03</a>",
    f"<a  href={cfg.base_url}/block/A03/scrapandstat>Scrap and build statistics</a>",
    f"<a href={cfg.base_url}/db_files>Show all db files</a>",
    f"<a href={cfg.base_url}/setbasedb>Set Base DB file for statistics</a>"
    ]
    urls_str = "<br>".join(urls_list)
    return urls_str

@kn_app.route('/ping')
def ping():
    return 'Pong', 201

@kn_app.route('/scrap')
def scrap():
    scrapper = KNScrapper(block='A03', min_floor=9, headless=True)
    db = scrapper.scrap()
    return jsonify(db)

@kn_app.route('/block/<block>/scrap')
def scrap_block(block):
    scrapper = KNScrapper(block=block, min_floor=9, headless=True)
    db = scrapper.scrap()
    db = {block: db}
    table_attributes = {"style" : "width:100%", "class" : "table table-striped"}
    db_table = json2table.convert(db, build_direction="TOP_TO_BOTTOM", table_attributes=table_attributes)
    return db_table

@kn_app.route('/block/<block>/scrapandstat')
def get_statistics(block):
    args = request.args
    show_empty_rooms = args.get('show', '')
    if show_empty_rooms == 'True':
        show = True
    else:
        show = False
    a = KNScrapper(block=block, min_floor=2, headless=True)
    #a.generate_room_str(7, 3)
    #a.main()
    db = {}
    db = a.scrap()
    t = str(datetime.now()).replace(' ', '-').replace('.', "-")
    t = datetime.now().strftime('%Y-%m-%d-%H_%M_%S')
    file_content = json.dumps(db, indent=4)
    filename = f'C:/_projects/kn_monitoring/data/db-{a.block}-{t}.json'
    with open(filename, 'w+') as f:
        f.write(file_content)

    # with open(filename, "r+") as f:
    #     db = json.loads(f.read())
    empty = a.statistics(db, show_empty_rooms=show)
    if show:
        print(empty)

    transfers = KnTransfers(new_db=filename, old_db=cfg.db_compare_base)
    with io.StringIO() as s:
        with redirect_stdout(s):
            transfers.compare(scrapper_class=KNScrapper)
        stat = s.getvalue()
    stat = stat.replace("\n", '<br>')
    return stat

@kn_app.route('/db_files')
def get_db_files():
    files = DbManagment().get_files()
    files_l = "<br>".join([f"<a href={cfg.base_url}/setbasedb/{f}>{f}</a>" for f in files])
    files_r = '<br>'.join(files)
    reference_db_file = cfg.db_compare_base
    output = f"{files_l}<br><br><b>Reference file for comparison{reference_db_file}</b>"
    return output

@kn_app.route('/room/<int:number>')
def get_persons_in_room(number):
    pass

@kn_app.route('/setbasedb/<filename>')
def set_db_base_file(filename):
    
    cfg.db_compare_base = cfg.data_path + '/' + filename
    return f"Base file is changed to {filename}.<br><a href=http://localhost:5000> Go to main page </a>"


if __name__=='__main__':
    kn_app.run(host='0.0.0.0', port=5000, debug=True)
