/**
 * Created by User on 07-Aug-17.
 */
function pokusaj(ref)
{


  /*  var htxp = new XMLHttpRequest();

                htxp.onreadystatechange = function()
                {
                    if(htxp.readyState==4 && htxp.status==200)
                        {
                            alert(htxp.responseText)

                        }

                }

					var json_upload = "json_name=" + JSON.stringify({'artikal':ref.toString()});
                               		 htxp.open("GET","http://localhost:8000/prodavnica/ajax/dodajUKorpu/");

//					htxp.open("POST", "http://localhost:8000/prodavnica/ajax/dodajUKorpu");
					htxp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
					htxp.send(json_upload);

*/

  $.ajax({url: "http://localhost:8000/prodavnica/ajax/dodajUKorpu",
                    data: {
                    'artikal': ref.toString()
                    },

                    success: function(result){
                    //$("#div1").html(result);
                        //document.getElementById("okvir").innerHTML="asdasd";
                       // document.getElementById("sadrzaj_korpe").innerHTML=result;


         }});

}

function dodajUKorpu(referenca)
{
    						    alert("asdasdasdadasd");
}

function obrisiIzKorpe(korpa_id,artikal_id,stavka_id,korisnik_id) {


  $.ajax({url: "http://localhost:8000/prodavnica/ajax/obrisiIzKorpe",
                    data: {
                    	'korpa_id': korpa_id,
						'artikal_id' :artikal_id,
						'stavka_id' : stavka_id,
						'korisnik_id' : korisnik_id
                    },

                    success: function(result){
                    //$("#div1").html(result);
                        //document.getElementById("okvir").innerHTML="asdasd";
                       // document.getElementById("sadrzaj_korpe").innerHTML=result;


						document.getElementById("sadrzaj_korpe").innerHTML=result

         }});

}

function finalizujKupovinu(korisnik_id)
{

			if((document.getElementById('adresa').value).length < 8) {
                document.getElementById('upozorenje_adresa').innerHTML = "Adresa mora imati minimalno 8 karaktera";
            	return;
			}
  $.ajax({url: "http://localhost:8000/prodavnica/ajax/finalizujKupovinu",
                    data: {
						'adresa' : document.getElementById('adresa').value,
						'korisnik_id' : korisnik_id
                    },

                    success: function(result){
                    //$("#div1").html(result);
                        //document.getElementById("okvir").innerHTML="asdasd";
                       // document.getElementById("sadrzaj_korpe").innerHTML=result;

						document.getElementById("sadrzaj_korpe").innerHTML="<h1>Hvala na kupovini</h1>";
						document.getElementById('upozorenje_adresa').innerHTML = "";



         }});
}

    $(function () {
        // Remove Search if user Resets Form or hits Escape!
		$('body, .navbar-collapse form[role="search"] button[type="reset"]').on('click keyup', function(event) {
			console.log(event.currentTarget);
			if (event.which == 27 && $('.navbar-collapse form[role="search"]').hasClass('active') ||
				$(event.currentTarget).attr('type') == 'reset') {
				closeSearch();
			}
		});

		function closeSearch() {
            var $form = $('.navbar-collapse form[role="search"].active')
    		$form.find('input').val('');
			$form.removeClass('active');
		}

		// Show Search if form is not active // event.preventDefault() is important, this prevents the form from submitting
		$(document).on('click', '.navbar-collapse form[role="search"]:not(.active) button[type="submit"]', function(event) {
			event.preventDefault();
			var $form = $(this).closest('form'),
				$input = $form.find('input');
			$form.addClass('active');
			$input.focus();

		});
		// ONLY FOR DEMO // Please use $('form').submit(function(event)) to track from submission
		// if your form is ajax remember to call `closeSearch()` to close the search container
		$(document).on('click', '.navbar-collapse form[role="search"].active button[type="submit"]', function(event) {
			event.preventDefault();
			var $form = $(this).closest('form'),
				$input = $form.find('input');
			$('#showSearchTerm').text($input.val());
            closeSearch()
		});
    });


function spasiPromjene()
{




            var artikal_id = document.getElementById("cuvajId").innerHTML;
            var nova_cijena = document.getElementById('nova_cijena').value;
            var novi_naziv = document.getElementById('novi_naziv').value;

            var er = /^[0-9]+$/;



            if( novi_naziv.length < 5)
                return;



            $.ajax({url: "http://localhost:8000/prodavnica/ajax/spasiPromjene/",

                    data: {
                    csrfmiddlewaretoken: '{{ csrf_token }}',
                    'artikal_id': artikal_id,
                        'nova_cijena':nova_cijena,
                        'novi_naziv':novi_naziv
                    },

                    success: function(result){
                    //$("#div1").html(result);
                        //document.getElementById("okvir").innerHTML="asdasd";
                       // document.getElementById("sadrzaj_korpe").innerHTML=result;

			location.href = "http://localhost:8000/prodavnica/zaposlenik";
         }});



}


function dajPretragu(page,naziv,minCijena,maxCijena) {

		sveKategorije = document.getElementsByClassName('kategorija');
            sviProizvodjaci = document.getElementsByClassName('proizvodjaci');
            kategorije = [];
            proizvodjaci = [];

            for(var i = 0; i < sveKategorije.length; i++)
            {
                if(sveKategorije[i].checked)
                    kategorije.push(sveKategorije[i].id)
            }
            for(i = 0; i < sviProizvodjaci.length; i++)
            {
                if(sviProizvodjaci[i].checked)
                    proizvodjaci.push(sviProizvodjaci[i].id)
            }




           $.ajax({url: "http://localhost:8000/prodavnica/pretraga/" + page,



               type:'POST',
                    data: {        csrfmiddlewaretoken: '{{ csrf_token }}',


                        'upit' : document.getElementById('upit').value,
                        'minCijena' : document.getElementById('minCijena').value,
                        'maxCijena' : document.getElementById('maxCijena').value,
                        'kategorije[]' : kategorije,
                        'proizvodjaci[]' : proizvodjaci

                    },

                    success: function(result){
               document.getElementById("sadrzaj_kataloga").innerHTML=result;


         }});

}


function dajKategoriju(page,kategorija,minCijena,maxCijena) {

		strink = "http://localhost:8000/prodavnica/filtriraj/" + page;
	$.ajax({
        url: strink,



        type: 'POST',
        data: {

                    csrfmiddlewaretoken: '{{ csrf_token }}',

            'kategorija': kategorija,
            'minCijena': document.getElementById('minCijena').value,
            'maxCijena': document.getElementById('maxCijena').value

        },

        success: function (result) {
            //$("#div1").html(result);
            //document.getElementById("okvir").innerHTML="asdasd";
            document.getElementById("sadrzaj_kataloga").innerHTML = result;
        }
    })
}