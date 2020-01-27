# FCurve helper

FCurve Helper is a blender addon designed to help in handling the fcurves.

 It is currently a work in progress, so a few things may be off, don’t hesitate to report any bugs

Here are the features :
- Add or Modify FCurves modifier : This operator allows user to setup and add a new modifier to all selected FCurves. It works in "Object mode" or in "Bone mode". It applies to all selected objects and selected FCurves. This can also be used to tweak existing modifier. For now, user will have to manually call the operator (search for it with F3 typing “fcurve” or set a shorcut for it) fcurvehelper.addmodifier
- Remove FCurves modifier : Remove FCurves modifier(s) for selected object by type, or all existing modifier
- Inspector : Check which FCurves have modifier. Next step is to add a few simple actions from this Inspector (Remove, Copy, Paste)
