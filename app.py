from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/escalas'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    if request.method == 'POST':
        departamento = request.form['departamento']
        mes_ano = request.form['mes_ano']
        rodape = request.form['rodape']
        funcoes = request.form.getlist('funcao')
        datas = request.form.getlist('data')

        nomes_por_funcao = {}
        for i, funcao in enumerate(funcoes):
            nomes_por_funcao[funcao] = request.form.getlist(f"nome_{i}")

        largura = 1000
        altura_linha = 60
        cabecalho_altura = 150
        rodape_altura = 120
        altura_total = cabecalho_altura + len(datas) * altura_linha + rodape_altura

        imagem = Image.new("RGB", (largura, altura_total), "black")
        draw = ImageDraw.Draw(imagem)

        try:
            fonte_titulo = ImageFont.truetype("arial.ttf", 40)
            fonte_coluna = ImageFont.truetype("arial.ttf", 28)
            fonte_conteudo = ImageFont.truetype("arial.ttf", 26)
            fonte_rodape = ImageFont.truetype("arial.ttf", 22)
        except:
            print("⚠️  Fonte 'arial.ttf' não encontrada. Usando fonte padrão.")
            fonte_titulo = ImageFont.load_default()
            fonte_coluna = ImageFont.load_default()
            fonte_conteudo = ImageFont.load_default()
            fonte_rodape = ImageFont.load_default()

        draw.text((largura/2, 20), departamento, font=fonte_titulo, fill="white", anchor="mm")
        draw.text((largura/2, 80), mes_ano, font=fonte_titulo, fill="white", anchor="mm")

        col_x = [100]
        for i in range(len(funcoes)):
            col_x.append(300 + i * 200)

        draw.text((col_x[0], cabecalho_altura), "DATA", font=fonte_coluna, fill="white")
        for i, funcao in enumerate(funcoes):
            draw.text((col_x[i+1], cabecalho_altura), funcao.upper(), font=fonte_coluna, fill="white")

        y = cabecalho_altura + 40
        cores_fundo = ["#3a3a3a", "#1f1f1f"]

        for idx, data in enumerate(datas):
            cor = cores_fundo[idx % 2]
            draw.rectangle([0, y - 10, largura, y + altura_linha - 10], fill=cor)
            draw.text((col_x[0], y), data, font=fonte_conteudo, fill="white")
            for i, funcao in enumerate(funcoes):
                nomes = nomes_por_funcao[funcao]
                if idx < len(nomes):
                    nome = nomes[idx].replace("—", "-")
                    draw.text((col_x[i+1], y), nome, font=fonte_conteudo, fill="white")
            y += altura_linha

        draw.text((largura/2, y + 20), rodape, font=fonte_rodape, fill="white", anchor="mm", align="center")

        filename = f"{UPLOAD_FOLDER}/escala_{departamento.replace(' ', '_')}.png"
        imagem.save(filename)

        return send_file(filename, mimetype='image/png', as_attachment=True, download_name=os.path.basename(filename))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
