"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const vscode = require("vscode");
const vscode_1 = require("vscode");
const jdocTools_1 = require("./jdocTools");
const open = require("open");
const consts = require("./Constants");
const fsUtils = require("./FSUtils");
const packageJSON = require('../package.json');
function activate(context) {
    console.log('Javadoc Tools is now active');
    showUpgradeNotification(context);
    let disposable = vscode_1.commands.registerCommand('javadoc-tools.jdocGenerate', () => __awaiter(this, void 0, void 0, function* () {
        const activeEditor = vscode_1.window.activeTextEditor;
        jdocTools_1.JdocTools.createJdocCommentsCurrFile();
        // vscode.window.showInformationMessage('Hello WorldForkers!');
    }));
    let disposable1 = vscode_1.commands.registerCommand('javadoc-tools.generateCommentsForWorkspace', () => {
        jdocTools_1.JdocTools.createJdocCommentsForWorkspace();
    });
    let disposable2 = vscode_1.commands.registerCommand('javadoc-tools.jdocGenerateFromContext', (uri) => {
        console.log(uri);
        jdocTools_1.JdocTools.openFile(uri);
        // activeWindow.createTreeView('explorer',[]);
    });
    context.subscriptions.push(vscode_1.commands.registerCommand('javadoc-tools.generateCommentsForMethod', () => __awaiter(this, void 0, void 0, function* () {
        const activeEditor = vscode_1.window.activeTextEditor;
        if (activeEditor) {
            let methodsCurrFile = jdocTools_1.JdocTools.getMethodFromCurrDocument(activeEditor);
            methodsCurrFile.then(resolveMethods => {
                if (resolveMethods) {
                    let items = Object.values(resolveMethods).map(item => ({
                        label: item.name
                    }));
                    // const quickPOptions = new vscode.qui
                    vscode.window
                        .showQuickPick(items, {
                        canPickMany: true,
                        placeHolder: 'Select the methods to generate Comments'
                    })
                        .then(resolveQP => {
                        if (resolveQP) {
                            let methodList = new Array();
                            for (const element of resolveQP) {
                                let checkMethod = resolveMethods.filter(method => method.name === element.label)[0];
                                if (checkMethod) {
                                    methodList.push(checkMethod);
                                }
                            }
                            if (methodList) {
                                jdocTools_1.JdocTools.processMethods(methodList, activeEditor);
                            }
                        }
                    });
                }
            });
        }
    })));
    let disposable3 = vscode_1.commands.registerCommand('javadoc-tools.exportJavadoc', () => {
        //get workspace src folder
        let fldrs = [];
        let srcFolder = vscode.workspace.getConfiguration().get('javadoc-tools.generateJavadoc.workspaceSourceFolder');
        if (!srcFolder) {
            srcFolder = vscode.workspace.rootPath + '\\src';
        }
        if (typeof srcFolder === 'string') {
            fldrs = fsUtils.getChildDir(srcFolder);
            fldrs = fldrs.filter(fldr => fsUtils.isDirectory(fldr[1]));
            // fldrs = fldrs.map(fldr => fldr[0]);
            console.log(fldrs);
        }
        console.log(srcFolder);
        let trgFolder = vscode.workspace.getConfiguration().get('javadoc-tools.generateJavadoc.targetFolder');
        if (!trgFolder) {
            trgFolder = vscode.workspace.rootPath + '\\javadoc';
        }
        console.log(trgFolder);
        let javaHome = vscode.workspace.getConfiguration().get('java.home');
        if (!javaHome) {
            javaHome = process.env.JAVA_HOME;
        }
        if (javaHome) {
            if (javaHome.endsWith('\\')) {
                javaHome.replace('\\$', '');
            }
        }
        let runMode = vscode.workspace.getConfiguration().get('javadoc-tools.generateJavadoc.runMode');
        if (fldrs) {
            let cmd = '"' +
                javaHome +
                '\\bin\\javadoc" ' +
                runMode +
                ' -d "' +
                trgFolder +
                '" -sourcepath "' +
                srcFolder +
                '" -subpackages ' +
                fldrs.map(fldr => fldr[0]).join(' ');
            let terminal = vscode_1.window.createTerminal('Export Javadoc');
            terminal.show();
            terminal.sendText(cmd);
        }
    });
    context.subscriptions.push(disposable, disposable1, disposable2, disposable3);
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
function showUpgradeNotification(context) {
    let instldVersion = context.globalState.get(consts.INSTL_VER);
    console.log(instldVersion);
    if (packageJSON.version !== instldVersion) {
        vscode.window
            .showInformationMessage(consts.CHNGLOG_MSG, consts.BTN_SHOW_CHNGLOG, consts.BTN_DONT_SHOW, consts.BTN_REMIND_LATER)
            .then(btn => {
            if (btn === consts.BTN_SHOW_CHNGLOG) {
                open(consts.CHNGLOG_URI);
                context.globalState.update(consts.INSTL_VER, packageJSON.version);
            }
            else if (btn === consts.BTN_DONT_SHOW) {
                context.globalState.update(consts.INSTL_VER, packageJSON.version);
            }
        });
    }
}
exports.showUpgradeNotification = showUpgradeNotification;
//# sourceMappingURL=extension.js.map