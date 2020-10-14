"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const path_1 = require("path");
function getChildDir(source) {
    return fs.readdirSync(source).map(fldr => [fldr, path_1.join(source, fldr)]);
}
exports.getChildDir = getChildDir;
function isDirectory(dir) {
    return fs.statSync(dir).isDirectory();
}
exports.isDirectory = isDirectory;
//# sourceMappingURL=FSUtils.js.map