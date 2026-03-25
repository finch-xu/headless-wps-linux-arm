#!/usr/bin/env python3
"""WPS Word转PDF Flask服务"""
import os
import uuid
import tempfile
from flask import Flask, request, send_file, jsonify
from pywpsrpc.rpcwpsapi import createWpsRpcInstance, wpsapi
from pywpsrpc.common import QtApp

# gunicorn fork后每个worker独立初始化Qt
_qt_app = QtApp(["wps-convert"])

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'.doc', '.docx', '.wps', '.txt', '.rtf'}


def _convert_word_to_pdf(input_path, output_path):
    """调用WPS RPC将Word文件转为PDF"""
    hr, rpc = createWpsRpcInstance()
    if hr != 0:
        raise RuntimeError(f"createWpsRpcInstance failed: hr={hr}")

    hr, wps = rpc.getWpsApplication()
    if hr != 0 or wps is None:
        raise RuntimeError(f"getWpsApplication failed: hr={hr}")

    wps.Visible = False

    try:
        hr, doc = wps.Documents.Open(input_path, ReadOnly=True)
        if hr != 0:
            raise RuntimeError(f"Documents.Open failed: hr={hr}")

        doc.SaveAs2(output_path, FileFormat=wpsapi.wdFormatPDF)
        doc.Close(wpsapi.wdDoNotSaveChanges)
    finally:
        wps.Quit(wpsapi.wdDoNotSaveChanges)


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({"error": "请上传file字段"}), 400

    file = request.files['file']
    if not file.filename:
        return jsonify({"error": "文件名为空"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": f"不支持的格式: {ext}，支持: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, f"input{ext}")
        output_path = os.path.join(tmpdir, f"{uuid.uuid4()}.pdf")

        file.save(input_path)

        try:
            _convert_word_to_pdf(input_path, output_path)
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 500

        pdf_name = os.path.splitext(file.filename)[0] + '.pdf'
        return send_file(output_path, mimetype='application/pdf',
                         download_name=pdf_name, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
