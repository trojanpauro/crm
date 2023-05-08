
// A $( document ).ready() block.
$( document ).ready(function() {






// begining of 
$('.buts').click(function (e) { 
	$('#agent_modal').modal('show');
	
});



$('.contact_buts').click(function (e) { 
	$('#contact_modal').modal('show');
	
});








// end of 




	

	$('.popy')
	.popup({
		popup: '.special.popup',
		delay: {
	show: 0,
	hide: 2000
}
	})
;
// end of 


// begining of 





	$( "#quantity" ).change(function() {
		 let  price = $("#quantity").attr('data-price');
		 let newValue = $("#quantity").val();
		let  total=price*newValue;
		$("#myTotal").text(total);
});

// end of 



// begining of 



	function Quickcheck_out(var1,var2){
	$("#quick_check_out_modal").modal({

	});


	let name=arguments[0];
	let price=arguments[1];
	let id  = arguments[2];
	let header_part="Express check_out for ";
	let header=header_part.concat(name);

	 $("#quick_quantity").attr("data-quickprice",price);
		$("#quick_total").text(price);
		$(".modal_header").text(header);
		$('#quick_product_id_input').val(id);
		$("#quick_check_out_modal").modal("show");
	}



	$( "#quick_quantity" ).change(function() {
		 let  quick_price = $("#quick_quantity").attr('data-quickprice');
		 let quick_new_value = $("#quick_quantity").val();
		let  quick_total=quick_price*quick_new_value;
		$("#quick_total").text(quick_total);
});


	 $("#quick_method").change(function() {

								var value = $("#quick_method").val();


								 if (value=="other"){
								 $("#quick_phone_number").hide();
								}

								else{
									$("#quick_phone_number").show();

								}
							})
	

// end of 





	 // this is the id of the form
$("#add_to_form").submit(function(e) {

		e.preventDefault();
		 // avoid to execute the actual submit of the form.
		 $("#my_dimmer").addClass("active");




		var form = $(this);
			$.ajax({
				url: form.attr("data-addtocart"),
				data: form.serialize(),
				csrfmiddlewaretoken: '{{ csrf_token }}',
				type: 'post',
				dataType: 'json',
				success: function (data) {
					$('#cart_total').text(data['cart_total']);
					$('#cart_items').text(data['cart_items']);
					$('#add_to_cart_btn').hide();
					$('#proceed').show();
					 $("#my_dimmer").removeClass("active");
						},

					error:function(){
					alert('error in request');
				},

				complete:function(){
							console.log("complete")
						}
			});


		});




	// end of 




	
	 // this is the id of the form
$("#quick_check_out_form").submit(function(e) {

		e.preventDefault(); // avoid to execute the actual submit of the form.


	var form = $(this);
			$.ajax({
				url: form.attr("data-quickcheck_out"),
				data: form.serialize(),
				csrfmiddlewaretoken: '{{ csrf_token }}',
				type: 'post',
				dataType: 'json',
				success: function (data) {
			
										if(data['message']=="successful" ){
							alert('transaction successful');

						}


						else if (data['message']=="response  failed") {

							alert('transation failed please  check  your balance and try again')

						}

						else{
					$(location).attr('href',data['link']);

						}

					},

					error:function(){
					alert('error in request');
				},

				complete:function(){
							console.log("complete")
						}
			});


		});




	// end of 




	// begining of 
		
$("#check_out_button").click(function(){

 $("#check_out_modal").modal({});

$("#check_out_modal").modal("show");

});


	// end of 


// begining of 
 $("#method").change(function() {

var value = $("#method").val();
								 if (value=="other"){
								 $("#phone_number").hide();
								}

								else{
									$("#phone_number").show();
								}
							})
// end of 




	
	 // this is the id of the form
$("#transact_form").submit(function(e) {

		e.preventDefault(); // avoid to execute the actual submit of the form.

		var form = $(this);
			$.ajax({
				url: form.attr("data-transact"),
				data: form.serialize(),
				csrfmiddlewaretoken: '{{ csrf_token }}',
				type: 'post',
				dataType: 'json',
				success: function (data) {
						if(data['message']=="successful" ){

								var pollingModal=$("#polling_modal")

								pollingModal.modal({});
								pollingModal.modal("show");



							 pollTransaction()
							}



						else if (data['message']=="response  failed") {

							alert('transaction failed')

						}

						else{
					$(location).attr('href',data['link']);

						}

					
					},

					error:function(){
					alert('error in request');
				},

				complete:function(){
							console.log("complete");
						}
			});


		});









								function pollTransaction(){
									polltrap=$('#polltrap')
									$.ajax({
										url: polltrap.attr("data-poll"),
										type: 'get',
										dataType: 'json',
										success: function (data) {



									var pollingModal=$("#polling_modal");
									pollingModal.modal("hide");
							if(data["message"]=="successful"){
								$("#payment_success_modal").modal({});
							 $("#payment_success_modal").modal("show");}


							 else{

										$("#payment_failure_modal").modal({});
													$("#payment_failure_modal").modal("show");
							 }





							
							 
									},
										error:function(){
											alert("network error please try again after some time")
										 
												},

										complete:function(){
												console.log("complete ")
												}
												});
	
											}



	// end of 



// begining of 
	

$('#pva-picker,#pva-picker2,\
	#unipaste_dye-picker,#unipaste_dye-picker2,\
	#gold_powders-picker,#gold_powders-picker2,\
	#oxides-picker,#oxides-picker2,\
	#water_based_dyes-picker,#water_based_dyes-picker2,\
	#poster_paints-picker,#poster_paints-picker2,\
	#undercoat-picker,#undercoat-picker2').spectrum({
	type: "text",
	showPaletteOnly: "true",
	hideAfterPaletteSelect: "true",
	palette: [
				[ "#ffe9ba",
					"#fdd7aa",
					"#e87a3f",
					"#d4794a",
					"#ffe7c1",
					"#e3c7a0",
					"#f8b684",
					"#f6cca4",
					"#e2d6be",
					"#fcd7ad"],
				[
					"#e9b586",
					"#dfc0a3",
					"#ecd5b5",
					"#f8c78c",
					"#e7cebc",
					"#b3a78d",
					"#f8dfc1",
					"#e6ac86",
					"#d99c70",
					"#cda8a2",],

					[

					"#b9a79b",
					"#86726b",
					"#f9af12",
					"#0c5c41",
					"#82552c",
					"#602f2b",
					"#fab300",
					"#08724e",
					"#925239",
					"#c42a2a",
					],
					[
					"#f19596",
					"#a6d1a3",
					"#a8babc",
					"#c5163d",
					"#985286",
					"#9cd1bd",
					"#a6a5a1",
					"#7d8184",
					"#b899c2",
					"#80c7b9"],
						[
					"#193f63",
					"#5483b9",
					"#482d26",
					"#0069ab",
					"#85a5d6",
					"#57141d",
					"#000000",
					"#2e2d29",
					"#86382e#",
					"#98d2e6",],
					[ "#bf0d0d",
					"#834b32",
					"#cdc2e2",
					"#a0a5a8",
					"#375940"
		]
	 
			
		]
});

// end of 


// begining of 
	

$('#gloss-picker ,#gloss-picker2').spectrum({
	type: "text",
	showPaletteOnly: "true",
	hideAfterPaletteSelect: "true",
	palette: [

			[
				"#83c49a",
				"#001739",
				"#6f8cb4",
				"#fee6b8",
				"#a1d2bc",
				"#034d66",
				"#af8a78",
				"#fee6b8",
				"#bedab1",
				"#006cad",],
					[
				"#d6a07e",
				"#fdedcb",
				"#cbd4b7",
				"#23a8d5",
				"#fbcb9d",
				"#fcded6",
				"#d3caad",
				"#3cb3c7",
				"#f7d9bd",
				"#958c7d"
					]
				
		]
});

// end of 



// begining of 

$('#roof_and_stoep-picker, #roof_and_stoep-picker2').spectrum({
	type: "text",
	showPaletteOnly: "true",
	hideAfterPaletteSelect: "true",
	palette: [

				"#265042",
				"#006227",
					"#1f9131",
					"#57141d",
					"#4c302c"]
});

// end of 

// begining of 
	

$('#roadline-picker,#roadline-picker2').spectrum({
	type: "text",
	showPaletteOnly: "true",
	hideAfterPaletteSelect: "true",
	palette: [

				"#fab300",
				"#ffffff"
					]
});


$('#stencil_black_ink-picker,#stencil_black_ink-picker2').spectrum({
	type: "text",
	showPaletteOnly: "true",
	hideAfterPaletteSelect: "true",
	palette: ["#000000"],
});


$('#tinters-picker,#tinters-picker2').spectrum({
	type: "text",
	showPaletteOnly: "true",
	hideAfterPaletteSelect: "true",
	palette: [
				"#fab300",
				"#fffff"
					]
});






// end of 

	
	





    
});




function showModal(var1,var2,var3){
	$("#add_to_cart_modal").modal({
		autofocus: false,

	 onHidden: function(){
     $(".modalpicker").hide();
      
    },
});


	let name=arguments[0];
	let price=arguments[1];
	let id  = arguments[2];
	let category =arguments[3];

	 $("#quantity").attr("data-price",price);
		$("#myTotal").text(price);
		$(".modal_header").text(name);
		$('#product_id_input').val(id);
		if (category=='pva'){
			$(".pva-picker").show();
					}

		else if(category=="gloss"){
			$("#gloss-picker").show();}
			

		else if(category=="roof_and_stoep"){
					$("#roof_and_stoep-picker").show();
				
		}
		else if(category=="unipaste_dye"){

			$("#pva-picker").show();
		
		}

		else if (category=="gold_powders"){
			$("#gold_powders-picker").show()
		
		}

		 else if (category=="water_based_dyes"){

			$("#water_based_dyes-picker").show();
			
		}


		 else if (category=="oxides"){

			$("#oxides-picker").show();
			
		}

		 else if (category=="stencil_black_ink"){
		 	$("#stencil_black_ink-picker").show();
			
		}



		 else if (category=="tinters"){
			$("#tinters-picker").show();
			
}

		 else if (category=="roadline"){
			$("#roadline-picker").show();
		

		}



		 else if (category=="poster_paints"){

			$("#poster_paints-picker").show();
		
		}

		else if (category=="undercoat"){

			$("#undercoat-picker").show();
			

		}

		else if (category=="other"){
			console.log("other");


		}


		$("#add_to_cart_modal").modal("show");
	}


