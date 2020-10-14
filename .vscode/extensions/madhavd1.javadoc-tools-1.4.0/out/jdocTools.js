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
const JAVADOC_START = "\n/** ";
const JAVADOC_PARAMS = '@param ';
const JAVADOC_THROWS = '@throws ';
const JAVADOC_RETURN = '@return ';
const JAVADOC_END = '\n */';
const ASTERISK = '\n * ';
const NEW_LINE = '\n';
const LOG_DELIMITER = '-------------------------------------------------------------------------------------------';
const acitveWorkspace = vscode.workspace;
const activeWindow = vscode.window;
class JdocTools {
    // static activeEditor : vscode.TextEditor | undefined = vscode.window.activeTextEditor;
    constructor() { }
    static createJdocCommentsCurrFile() {
        return __awaiter(this, void 0, void 0, function* () {
            let activeEditor = activeWindow.activeTextEditor;
            if (activeEditor) {
                console.log("Processing File: " + activeEditor.document.fileName);
                console.log(NEW_LINE + LOG_DELIMITER);
                let methods = yield this.getMethodFromCurrDocument(activeEditor);
                if (!methods) {
                    return;
                }
                else {
                    yield this.processMethods(methods.map((element) => {
                        if (element.kind = 5) {
                            return element;
                        }
                    }), activeEditor);
                }
                console.log(LOG_DELIMITER);
            }
            else {
                return;
            }
        });
    }
    static createJdocCommentsForWorkspace() {
        return __awaiter(this, void 0, void 0, function* () {
            if (acitveWorkspace) {
                let allFiles = yield acitveWorkspace.findFiles('**/*.java');
                for (let currFile of allFiles) {
                    let fileURI = vscode.Uri.file(currFile.fsPath);
                    let textDoc = yield acitveWorkspace.openTextDocument(fileURI);
                    let textEditor = yield activeWindow.showTextDocument(textDoc);
                    yield this.createJdocCommentsCurrFile();
                }
            }
        });
    }
    static openFile(uri) {
        let fileURI = vscode.Uri.file(uri.fsPath);
        acitveWorkspace.openTextDocument(fileURI).then((textDoc) => activeWindow.showTextDocument(textDoc).then((textEditor) => this.createJdocCommentsCurrFile()));
    }
    // await acitveWorkspace.findFiles('**/*.java').then(async (allFiles: any) => {
    //     await allFiles.forEach(async (currFile: { fsPath: string; }) => {
    //         let fileURI = vscode.Uri.file(currFile.fsPath);
    //         await acitveWorkspace.openTextDocument(fileURI).then(async (doc: any) => {
    //             console.log('changing doc to '+fileURI);
    //             await activeWindow.showTextDocument(doc,undefined,true).then(async (textEditor) => {
    //                  await this.createJdocCommentsCurrFile(textEditor);
    //             });
    //         });
    //     });
    // });
    static processMethods(methods, activeEditor) {
        let jdOffset = 0;
        methods.forEach(methodObj => {
            if (methodObj) {
                // let methodRange:vscode.Range= ;
                let methodDefnText = "";
                let defnFoundBoolean = false;
                let lineIndex = 0;
                let existingJdoc = this.checkJdocExists(methodObj, activeEditor);
                let multiLineComment = false;
                if (!existingJdoc) {
                    do {
                        let currLine = activeEditor.document.lineAt(methodObj.range.start.line + lineIndex).text.trim(); // getText(methodObj.range);
                        if (currLine.endsWith('{')) {
                            defnFoundBoolean = true;
                        }
                        let returnArray = this.StripComments(currLine, multiLineComment);
                        methodDefnText = methodDefnText + returnArray[0];
                        multiLineComment = returnArray[1];
                        lineIndex++;
                    } while (!defnFoundBoolean);
                    console.log(methodDefnText);
                    // methodDefnText = methodText.substring(0, methodText.indexOf("{")).trim();//Complete method definition. May contain existing javadoc
                    methodDefnText = this.removeOthers(methodDefnText);
                    let tagArray = new Map();
                    let javadocString = ""; //The final Javadoc string that will be inserted
                    let targetPosition = methodObj.range.start.with(methodObj.range.start.line + jdOffset, methodObj.range.start.character);
                    //Start Processing params
                    let paramStartIndex = methodDefnText.indexOf("(");
                    let paramEndIndex = methodDefnText.lastIndexOf(")");
                    let paramString = methodDefnText.substring(paramStartIndex + 1, paramEndIndex).trim();
                    let paramList;
                    if (paramString !== undefined && paramString !== "") {
                        paramList = paramString.split(",").map((element) => element.trim().split(" ").slice(-1).pop());
                    }
                    else {
                        console.log("No Params Found for: " + methodObj.name);
                        // vscode.window.showInformationMessage('No @Params Found for: ' + methodObj.name);
                    }
                    let throwsIndex = methodDefnText.lastIndexOf('throws');
                    let throwsList;
                    if (throwsIndex > -1) {
                        throwsList = methodDefnText.substr(throwsIndex + 6, methodDefnText.length).trim().split(",").map((element) => element.trim());
                    }
                    //Format the Param Strings
                    if (paramList) {
                        // console.log(paramList);
                        paramList.forEach(param => {
                            javadocString += ASTERISK + JAVADOC_PARAMS + param;
                            jdOffset += 1;
                        });
                    }
                    //Format the Return String
                    let returnType = methodObj.detail.substring(methodObj.detail.indexOf(":") + 1, methodObj.detail.length).trim(); //detail is in fact the return type
                    if (returnType !== 'void') {
                        javadocString += ASTERISK + JAVADOC_RETURN + returnType;
                        jdOffset += 1;
                    }
                    //Format the Throws Strings
                    if (throwsList) {
                        throwsList.forEach(ex => {
                            javadocString += ASTERISK + JAVADOC_THROWS + ex;
                            jdOffset += 1;
                        });
                    }
                    if (javadocString !== "") {
                        let finalJDocString = new vscode.SnippetString(JAVADOC_START + javadocString + JAVADOC_END + NEW_LINE);
                        activeEditor.insertSnippet(finalJDocString, targetPosition);
                        jdOffset += 3;
                    }
                }
            }
        });
    }
    static getDocumentSymbols(activeEditor) {
        return __awaiter(this, void 0, void 0, function* () {
            let symbols = yield vscode.commands.executeCommand('vscode.executeDocumentSymbolProvider', activeEditor.document.uri);
            return symbols;
        });
    }
    static getMethodsFromDocumentSymbols(symbols) {
        if (symbols) {
            let javaClassObj = symbols.find(element => element.kind === vscode.SymbolKind.Class);
            return javaClassObj ? javaClassObj.children.filter(element => element.kind === vscode.SymbolKind.Method) : undefined;
        }
        else {
            this.SymbolsNotFound();
            return;
        }
    }
    static NoMethodsFound() {
        console.log("No Methods Found");
        vscode.window.showInformationMessage('No Methods found in current File');
    }
    static SymbolsNotFound() {
        console.log("No Symbols Found");
        vscode.window.showInformationMessage('No Symbols found in current File');
    }
    static checkJdocExists(methodObj, activeEditor) {
        let existingJdoc;
        let methodText;
        if (methodObj) {
            methodText = activeEditor.document.getText(methodObj.range);
            let methodDefnText = methodText.substring(0, methodText.indexOf("{")).trim(); //Complete method definition. May contain existing javadoc
            // const regex = /([\s]*(@param|@throws)+[\s]+(.+))/g;
            // const tagsRegex = /((@param|@throws|@see|@returns|@author){1}[\s]+[\n]*([a-zA-Z_$]*)[\s\n]+(.+))/g;
            const tagsRegex = /((@param|@throws|@see|@returns|@author){1}[\s]+[\n]*([a-zA-Z_$0-9\s\n*]*))/g;
            if (methodDefnText.startsWith("/**") && methodDefnText.indexOf('*/') > -1) {
                existingJdoc = methodDefnText.substring(0, methodDefnText.indexOf("*/") + 2).trim();
                // let m;
                // if ((m = existingJdoc.match(tagsRegex)) !== null) {
                // 	let s = m.map(ele => ele.trim().split(" "));
                // 	console.log(m);
                // 	// m.forEach((match) => {
                // 	// 	jdArray.push(match);
                // 	// 	console.log(match);
                // 	// });
                // }
            }
            else if (methodDefnText.indexOf("/**") > -1) {
                existingJdoc = methodDefnText.substring(methodDefnText.indexOf("/**"), methodDefnText.lastIndexOf("*/") + 2).trim();
            }
        }
        return existingJdoc;
    }
    static StripComments(currLine, multiLineComment) {
        let originalText = currLine.trim();
        let evaluateMore = false;
        let javadocCommentStart = currLine.indexOf('/**');
        let multiLineCommentStart = currLine.indexOf('/*');
        let multiLineCommentEnd = currLine.indexOf('*/');
        let lineComment = currLine.indexOf('//');
        if (currLine === "" || currLine === undefined) {
            return ["", false];
        }
        if (currLine.startsWith("//")) { //check if this is a line comment. Iff true then return blank
            return ["", false];
        }
        else if (currLine.startsWith('/**') || currLine.startsWith('/*') || multiLineComment) { //Check if this is beginning a multi line comment
            if (currLine.endsWith('*/')) { //if comment ends in same line, return blank
                return ["", false];
            }
            else { //if comment end is not the last characted
                if (multiLineCommentEnd > -1 && multiLineCommentEnd < currLine.length - 1) { //redundant check to make sure that comment does not end in same line
                    // if (endIndex < currLine.length - 1) {
                    return this.StripComments(currLine.substring(multiLineCommentEnd, currLine.length).trim()); //In case it ends in same line before the end of actual line, strip the comment part
                    // evaluateMore=true;
                    // console.log(returnText);
                    // }
                }
                else { //else return blank - same as currLine.endsWith('*/')
                    return ["", true];
                }
            }
        }
        else if (currLine.startsWith('@')) { //ignoring this for now. Annotations to be handled in later release
            return ["", false];
        }
        else if (lineComment > 1) { //if the comment starts in the middle of the line
            return this.StripComments(currLine.substring(0, lineComment));
        }
        else if (multiLineCommentStart > 0) { //if multiline or javadoc comment start 
            if (!currLine.endsWith('*/') && multiLineCommentEnd > -1) { //if the comment ends mid-line
                return this.StripComments(currLine.substring(0, multiLineCommentStart) + currLine.substring(multiLineCommentEnd + 2, currLine.length));
            }
            else if (!currLine.endsWith('*/') && multiLineCommentEnd < 0) { //if there is no comment end in the line
                return this.StripComments(currLine.substring(0, multiLineCommentStart), true);
            }
            else if (currLine.endsWith('*/')) { //if the comment ends at the line end
                return this.StripComments(currLine.substring(0, multiLineCommentStart));
            }
        }
        else if (javadocCommentStart > 0) { //if multiline or javadoc comment start 
            if (!currLine.endsWith('*/') && multiLineCommentEnd > -1) {
                return this.StripComments(currLine.substring(0, multiLineCommentStart) + currLine.substring(multiLineCommentEnd + 2, currLine.length));
            }
            else if (!currLine.endsWith('*/') && multiLineCommentEnd < 0) {
                return this.StripComments(currLine.substring(0, multiLineCommentStart), true);
            }
            else if (currLine.endsWith('*/')) {
                return this.StripComments(currLine.substring(0, javadocCommentStart));
            }
        }
        else if (currLine.indexOf('{') > -1) {
            return this.StripComments(currLine.substring(0, currLine.indexOf('{')));
        }
        else if (currLine.indexOf('*') > -1) {
            if (multiLineCommentEnd > -1 && !currLine.endsWith('*/')) {
                return this.StripComments(currLine.substring(multiLineCommentEnd + 1, currLine.length));
            }
            else if (multiLineCommentEnd > -1 && currLine.endsWith('*/')) {
                return ["", false];
            }
            else {
                return ["", false];
            }
        }
        return [currLine.trim(), false];
    }
    static removeOthers(methodDefnText) {
        let genericStart = methodDefnText.indexOf('<');
        let genericEnd = methodDefnText.indexOf('>');
        //Remove generics. The comma in generics mess with the logic
        if (genericEnd - genericStart > 1) {
            return this.removeOthers(methodDefnText.substring(0, genericStart) + methodDefnText.substring(genericEnd + 1, methodDefnText.length));
        }
        return methodDefnText;
    }
    static getMethodFromCurrDocument(activeEditor) {
        return __awaiter(this, void 0, void 0, function* () {
            let symbols = yield this.getDocumentSymbols(activeEditor);
            let methods = this.getMethodsFromDocumentSymbols(symbols);
            return methods;
        });
    }
}
exports.JdocTools = JdocTools;
//# sourceMappingURL=jdocTools.js.map