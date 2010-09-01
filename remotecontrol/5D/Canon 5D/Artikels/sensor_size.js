// Javascript copyright Sean T. McHugh
//Cambridge in Colour Photography

<!-- Begin Focal Length Multiplier Calculator
function flmcalc(flmform) {
flmcoc = flmform.flmformat.value;
flmfocal = flmform.flmfocal.value;
if (isNaN(flmfocal)) {
alert('Gelieve een getal in te voeren voor de brandpuntsafstand.');
document.flmform.flmfocal.focus();
document.flmform.flmfocal.select();
}
else {
flm = 0.032 / flmcoc;
fullframefocal = flm * flmfocal;
flmform.flm.value = Math.round(10 * flm) / 10;
flmform.fullframefocal.value = Math.round(fullframefocal) + " mm";
   }
}
//  End Focal Length Multiplier Calculator -->

<!-- Begin Depth of Field Equivalents Calculator
function dofequivcalc(dofform) {
dofformat1 = dofform.dofformat1.value;
dofformat2 = dofform.dofformat2.value;
dofaperture = dofform.dofaperture.value;
doffocal = dofform.doffocal.value;
if (isNaN(doffocal)) {
alert('Gelieve een getal in te voeren voor de brandpuntsafstand.');
document.dofform.doffocal.focus();
document.dofform.doffocal.select();
}
else {
dofflm = dofformat2 / dofformat1;
reqfocal = dofflm * doffocal;
reqaperture = dofflm * dofaperture;
dofform.reqfocal.value = Math.round(reqfocal) + " mm";
dofform.reqaperture.value = Math.round(10 * reqaperture) / 10;
   }
}
//  End Depth of Field Equivalents Calculator -->

<!-- Begin Diffraction Limited Aperture Calculator
function diffapcalc(difform) {
diffcoc = difform.diffcoc.value;
megapixels = difform.megapixels.value;

if (isNaN(megapixels)) {
	alert('Gelieve een getal in te voeren voor de brandpuntsafstand.');
	document.difform.megapixels.focus();
	document.difform.megapixels.select();
	}
else {

if (diffcoc <= 0.0165) {
	pixelsize = (diffcoc / 0.032) * 36000 / Math.sqrt(4/3 * megapixels * 1e6); //in microns
	}
	else {
	pixelsize = (diffcoc / 0.032) * 36000 / Math.sqrt(3/2 * megapixels * 1e6); //in microns
	}
diffaperture = 2 * pixelsize / ( 2.43932 * 510e-9 * 1e6 ); //in f-stops
difform.diffaperture.value = Math.round(10 * diffaperture) / 10;
	}
}
//  End Diffraction Limited Aperture Calculator Calculator -->
















