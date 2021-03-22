$(document).ready(function() {
  validate();
  $('input').on('keyup', validate);
});

function validate() {
  var inputsWithValues = 0;

  // get all input fields except for type='submit'
  var myInputs = $("input:not([type='submit'])");

  myInputs.each(function(e) {
    // if it has a value, increment the counter
    if ($(this).val()) {
      inputsWithValues += 1;
    }
  });

  if (inputsWithValues == myInputs.length) {
    $("input[type=submit]").prop("disabled", false);
  } else {
    $("input[type=submit]").prop("disabled", true);
  }
}













$(document).ready(function(){
  var i=0;
  var counter = 0;
  $('#add').click(function(){
        counter++;
        document.getElementById("khara").value = counter;
        i++;
$('#dynamic_field').append('<div id="row'+i+'"> <div class="form-group "> <div class="insidedynamic"> <div class="row"> <div class="col-12 col-md-3"> <input autocomplete="off" autofocus class="form-control" name="thename'+i+'[]" placeholder="الاسم" type="text"> </div> <div class="col-12 col-md-3"> <input autocomplete="off" autofocus class="form-control" name="age'+i+'[]" placeholder="السن" type="text"> </div> <div class="col-12 col-md-3"> <select class="form-control" name="relationship'+i+'[]"> <option  selected="" value="لم يتم التحديد">الدور الأسري</option> <option value="رب الأسرة">رب الأسرة</option> <option value="الزوجة">الزوجة</option> <option value="الأم/الأب">الأم/الأب</option> <option value="الأخ/الأخت">الأخ/الأخت</option> <option value="الأبن/الأبنة">الأبن/الأبنة</option> <option value="الحفيد/الحفيدة">الحفيد/الحفيدة</option> </select>                    </div> <div class="col-12 col-md-3"> <select class="form-control" name="socialstate'+i+'[]"> <option  selected="" value="لم يتم التحديد">الحالة الإجتماعية</option> <option value="أعزب/عازبة">أعزب/عازبة</option> <option value="متزوج/متزوجة">متزوج/متزوجة</option> <option value="مطلق/مطلقة">مطلق/مطلقة</option> <option value="ارمل/أرملة">ارمل/ارملة</option> <option value="متوفي/متوفية">متوفي/متوفية</option> </select> </div> </div> <div class="row"> <div class="col-12 col-md-3"> <select class="form-control" name="healthstate'+i+'[]"> <option  selected="" value="لم يتم التحديد">الحالة الصحية</option> <option value="جيدة">جيدة</option> <option value="متوسطة">متوسطة</option> <option value="متهدورة">متدهورة</option> <option value="5%">5%</option> <option value="متوفي/متوفية">متوفي/متوفية</option> </select> </div> <div class="col-12 col-md-3"> <select class="form-control" name="degree'+i+'[]"> <option  selected="" value="لم يتم التحديد">المؤهل الدراسي</option> <option value="أمي">أمي</option> <option value="محو أمية">محو امية</option> <option value="الإبتدائية">الإبتدائية</option> <option value="الإعدادية">الإعدادية</option> <option value="دبلوم">دبلوم</option> <option value="ثانوي">ثانوي</option> <option value="مؤهل فوق متوسط">مؤهل فوق متوسط</option> <option value="مؤهل عالي">بكالريوس</option> <option value="درسات عليا">درسات عليا وما بعدها</option> </select> </div> <div class="col-12 col-md-3"> <input class="form-control" name="job'+i+'"  placeholder="الوظيفة" type="text"> </div> <div class="col-12 col-md-3"> <input class="form-control" name="salary'+i+'"  placeholder="الراتب" type="text"> </div> </div> </div> </div> <td><button type="button" name="remove" id="'+i+'" class="btn btn-danger submittt btn_remove">حذف الفرد</button></td></div>');      });
  $(document).on('click', '.btn_remove', function(){
       var button_id = $(this).attr("id");
       $('#row'+button_id+'').remove();
       i--;
       counter--;
       document.getElementById("khara").value = counter;
  });

});

