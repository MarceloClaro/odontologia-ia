#!/usr/bin/env python3
"""
Gerador de QR Codes — OdontoIA: Livro Imersão
SPEC-951-R200
Autor: Edson Laranjeiras

Gera QR codes para cada capítulo do livro nos 5 tipos:
🎬 Vídeo | 💻 Colab | 🧪 Testes | 🗣️ Podcast | 🔗 Referências
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from pathlib import Path
import json

# ---------------------------------------------------------------------------
# Configuração dos Capítulos
# ---------------------------------------------------------------------------

CAPITULOS = {
    1:  "parte1-fundamentos/historia-ia-odontologia",
    2:  "parte1-fundamentos/introducao-ia",
    3:  "parte1-fundamentos/python-odontologia",
    4:  "parte2-teoria/imagens-odontologicas",
    5:  "parte2-teoria/cnns-diagnostico",
    6:  "parte2-teoria/segmentacao-semantica",
    7:  "parte2-teoria/radiologia-dl",
    8:  "parte3-engenharia/sdd",
    9:  "parte3-engenharia/tdd",
    10: "parte3-engenharia/projetos-guiados",
    11: "parte3-engenharia/interpretacao",
    12: "parte4-aplicacoes/periodontia",
    13: "parte4-aplicacoes/gemeos-digitais",
    14: "parte4-aplicacoes/llms-rag",
    15: "parte4-aplicacoes/futuro-etica",
    16: "parte4-aplicacoes/implantodontia",
    17: "parte4-aplicacoes/ortodontia",
    18: "parte4-aplicacoes/cancer-oral",
    19: "parte4-aplicacoes/modelos-fundacionais",
    20: "parte5-futuro/publicacao-cientifica",
    21: "parte5-futuro/etica-lgpd",
    22: "parte5-futuro/educacao",
    23: "parte5-futuro/hospitais-virtuais",
    24: "parte5-futuro/conclusao",
}

TIPOS_QR = {
    "video": {"icone": "🎬", "subdominio": "video", "label": "Vídeo do Capítulo"},
    "colab": {"icone": "💻", "subdominio": "colab", "label": "Notebook Google Colab"},
    "testes": {"icone": "🧪", "subdominio": "testes", "label": "Testes TDD"},
    "podcast": {"icone": "🗣️", "subdominio": "podcast", "label": "Podcast do Capítulo"},
    "referencias": {"icone": "🔗", "subdominio": "refs", "label": "Referências"},
}

BASE_URL = "https://odontologia-ia.edsonlaranjeiras.com.br"

# ---------------------------------------------------------------------------
# Gerador de QR Codes
# ---------------------------------------------------------------------------

class GeradorQRCode:
    """Gera QR codes estilizados para o livro OdontoIA."""

    def __init__(self, output_dir: str = "ilustracoes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.manifest = []

    def gerar_todos(self):
        """Gera QR codes para todos os capítulos e tipos."""
        for cap_num in sorted(CAPITULOS.keys()):
            self._gerar_para_capitulo(cap_num)
        self._salvar_manifest()

    def _gerar_para_capitulo(self, cap_num: int):
        """Gera 5 QR codes para um capítulo."""
        rota = CAPITULOS[cap_num]
        for tipo, info in TIPOS_QR.items():
            url = f"{BASE_URL}/{info['subdominio']}/{rota}"
            nome_arquivo = f"qrcode-cap{cap_num:02d}-{tipo}.png"
            self._gerar_qrcode(url, nome_arquivo, cap_num, tipo)

    def _gerar_qrcode(self, url: str, nome_arquivo: str, cap_num: int, tipo: str):
        """Gera um QR code estilizado."""
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Criar imagem estilizada
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color="black",
            back_color="white",
        )

        caminho = self.output_dir / nome_arquivo
        img.save(caminho)

        self.manifest.append({
            "capitulo": cap_num,
            "tipo": tipo,
            "icone": TIPOS_QR[tipo]["icone"],
            "url": url,
            "arquivo": str(caminho),
        })

        print(f"  ✓ {nome_arquivo} → {url}")

    def _salvar_manifest(self):
        """Salva manifest JSON com todos os QR codes gerados."""
        manifest_path = self.output_dir / "qrcodes-manifest.json"
        with open(manifest_path, "w") as f:
            json.dump({
                "total": len(self.manifest),
                "base_url": BASE_URL,
                "qrcodes": self.manifest,
            }, f, indent=2, ensure_ascii=False)
        print(f"\n📋 Manifest salvo: {manifest_path}")
        print(f"   Total: {len(self.manifest)} QR codes gerados")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Gerador de QR Codes — OdontoIA Livro Imersão"
    )
    parser.add_argument(
        "--output", "-o",
        default="ilustracoes",
        help="Diretório de saída para as imagens",
    )
    parser.add_argument(
        "--capitulo", "-c",
        type=int,
        help="Gerar QR apenas para um capítulo específico",
    )
    
    args = parser.parse_args()
    
    gerador = GeradorQRCode(output_dir=args.output)
    
    print(f"\n{'='*50}")
    print("📱 GERADOR DE QR CODES — ODONTOIA")
    print(f"{'='*50}")
    print(f"URL Base: {BASE_URL}")
    print(f"Saída:    {args.output}/")
    print(f"{'='*50}\n")
    
    if args.capitulo:
        if args.capitulo in CAPITULOS:
            gerador._gerar_para_capitulo(args.capitulo)
        else:
            print(f"⚠️  Capítulo {args.capitulo} não encontrado.")
            print(f"   Capítulos disponíveis: {sorted(CAPITULOS.keys())}")
    else:
        gerador.gerar_todos()
    
    print(f"\n{'='*50}")
    print("✅ QR Codes gerados com sucesso!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
