#!/usr/bin/env python3
"""WPS RPC 文档转换脚本 — 支持 docx/xlsx/pptx 转 PDF"""
import sys
import os
import time


def convert_to_pdf(input_path, output_path):
    from pywpsrpc.rpcwpsapi import createWpsRpcInstance, wpsapi

    ext = os.path.splitext(input_path)[1].lower()

    if ext in ('.doc', '.docx', '.wps', '.txt', '.rtf'):
        _convert_wps(input_path, output_path)
    elif ext in ('.xls', '.xlsx', '.et', '.csv'):
        _convert_et(input_path, output_path)
    elif ext in ('.ppt', '.pptx', '.dps'):
        _convert_wpp(input_path, output_path)
    else:
        print(f"不支持的格式: {ext}")
        sys.exit(1)


def _convert_wps(input_path, output_path):
    from pywpsrpc.rpcwpsapi import createWpsRpcInstance, wpsapi

    hr, rpc = createWpsRpcInstance()
    if hr != 0:
        print(f"createWpsRpcInstance failed: hr={hr}")
        sys.exit(1)

    hr, app = rpc.getWpsApplication()
    if hr != 0 or app is None:
        print(f"getWpsApplication failed: hr={hr}")
        sys.exit(1)

    app.Visible = False

    hr, doc = app.Documents.Open(input_path, ReadOnly=True)
    if hr != 0:
        print(f"Documents.Open failed: hr={hr}")
        app.Quit(wpsapi.wdDoNotSaveChanges)
        sys.exit(1)

    doc.SaveAs2(output_path, FileFormat=wpsapi.wdFormatPDF)
    doc.Close(wpsapi.wdDoNotSaveChanges)
    app.Quit(wpsapi.wdDoNotSaveChanges)
    print(f"转换完成: {output_path}")


def _convert_et(input_path, output_path):
    from pywpsrpc.rpcetapi import createEtRpcInstance, etapi

    hr, rpc = createEtRpcInstance()
    if hr != 0:
        print(f"createEtRpcInstance failed: hr={hr}")
        sys.exit(1)

    hr, app = rpc.getEtApplication()
    if hr != 0 or app is None:
        print(f"getEtApplication failed: hr={hr}")
        sys.exit(1)

    app.Visible = False

    hr, wb = app.Workbooks.Open(input_path, ReadOnly=True)
    if hr != 0:
        print(f"Workbooks.Open failed: hr={hr}")
        app.Quit()
        sys.exit(1)

    wb.ExportAsFixedFormat(0, output_path)  # 0 = xlTypePDF
    wb.Close(False)
    app.Quit()
    print(f"转换完成: {output_path}")


def _convert_wpp(input_path, output_path):
    from pywpsrpc.rpcwppapi import createWppRpcInstance, wppapi

    hr, rpc = createWppRpcInstance()
    if hr != 0:
        print(f"createWppRpcInstance failed: hr={hr}")
        sys.exit(1)

    hr, app = rpc.getWppApplication()
    if hr != 0 or app is None:
        print(f"getWppApplication failed: hr={hr}")
        sys.exit(1)

    hr, pres = app.Presentations.Open(input_path, ReadOnly=True, WithWindow=False)
    if hr != 0:
        print(f"Presentations.Open failed: hr={hr}")
        app.Quit()
        sys.exit(1)

    pres.SaveAs(output_path, wppapi.OnlyPDF)
    pres.Close()
    app.Quit()
    print(f"转换完成: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"用法: {sys.argv[0]} <输入文件> <输出PDF>")
        print(f"示例: {sys.argv[0]} /docs/input.docx /docs/output.pdf")
        sys.exit(1)

    from pywpsrpc.common import QtApp
    QtApp(sys.argv)

    convert_to_pdf(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]))
