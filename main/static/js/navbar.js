// ---------Responsive-navbar-active-animation-----------
function test(){
	var tabsNewAnim = $('#navbarSupportedContent');
	var selectorNewAnim = $('#navbarSupportedContent').find('li').length;
	var activeItemNewAnim = tabsNewAnim.find('.active');
	var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
	var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
	var itemPosNewAnimTop = activeItemNewAnim.position();
	var itemPosNewAnimLeft = activeItemNewAnim.position();
	$(".hori-selector").css({
		"top":itemPosNewAnimTop.top + "px", 
		"left":itemPosNewAnimLeft.left + "px",
		"height": activeWidthNewAnimHeight + "px",
		"width": activeWidthNewAnimWidth + "px"
	});
	$("#navbarSupportedContent").on("click","li",function(e){
		$('#navbarSupportedContent ul li').removeClass("active");
		$(this).addClass('active');
		var activeWidthNewAnimHeight = $(this).innerHeight();
		var activeWidthNewAnimWidth = $(this).innerWidth();
		var itemPosNewAnimTop = $(this).position();
		var itemPosNewAnimLeft = $(this).position();
		$(".hori-selector").css({
			"top":itemPosNewAnimTop.top + "px", 
			"left":itemPosNewAnimLeft.left + "px",
			"height": activeWidthNewAnimHeight + "px",
			"width": activeWidthNewAnimWidth + "px"
		});
	});
}
$(document).ready(function(){
	setTimeout(function(){ test(); });
});
$(window).on('resize', function(){
	setTimeout(function(){ test(); }, 500);
});
$(".navbar-toggler").click(function(){
	$(".navbar-collapse").slideToggle(300);
	setTimeout(function(){ test(); });
});



// --------------add active class-on another-page move----------
jQuery(document).ready(function($){
	// Get current path and find target link
	var path = window.location.pathname.split("/").pop();

	// Account for home page with empty path
	if ( path == '' ) {
		path = 'index.html';
	}

	var target = $('#navbarSupportedContent ul li a[href="'+path+'"]');
	// Add active class to target link
	target.parent().addClass('active');
});





// Add active class on another page linked (version 1)
// ==========================================
// $(window).on('load',function () {
//     var current = location.pathname;
//     console.log(current);
//     $('#navbarSupportedContent ul li a').each(function(){
//         var $this = $(this);
//         // if the current path is like this link, make it active
//         if($this.attr('href').indexOf(current) !== -1){
//             $this.parent().addClass('active');
//             $this.parents('.menu-submenu').addClass('show-dropdown');
//             $this.parents('.menu-submenu').parent().addClass('active');
//         }else{
//             $this.parent().removeClass('active');
//         }
//     })
// });

// Add active class on another page linked (version 2)
// ==========================================
$(function () {
    var location = window.location.href;
    var cur_url = '/' + location.split('/').pop();
 
    $('#navbarSupportedContent ul li').each(function () {
        var link = $(this).find('a').attr('href');
 
        if (cur_url == link) {
            $(this).addClass('active');
        }
    });
});



// Add AJAX method
// ==========================================
// $(document).ready(function() {

//     // Check for hash value in URL
//     // var hash = window.location.hash.substr(1);
//     // var href = $('#navbarSupportedContent ul li a').each(function(){
//     //     var href = $(this).attr('href');
//     //     if(hash==href.substr(0,href.length-5)){
//     //         var toLoad = hash+'.html #content';
//     //         $('#content').load(toLoad)
//     //     } 
//     // });


// 	$('#navbarSupportedContent ul li a').click(function(){
//         var toLoad = $(this).attr('href')+' #content';
//         $('#content').hide('fast',loadContent);
//         $('#load').remove();
//         $('#wrapper').append('<span id="load">LOADING...</span>');
//         $('#load').fadeIn('normal');
//         function loadContent() {
//             $('#content').load(toLoad,'',showNewContent())
//         }
//         function showNewContent() {
//             $('#content').show('normal',hideLoader());
//         }
//         function hideLoader() {
//             $('#load').fadeOut('normal');
//         }
//         return false;
    
//     });
// });