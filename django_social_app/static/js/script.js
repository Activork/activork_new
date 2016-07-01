$(document).ready(function(){
	
	//Check to see if the window is top if not then display button
	$(window).scroll(function(){
		if ($(this).scrollTop() > 100) {
			$('.scrollToTop').fadeIn();
		} else {
			$('.scrollToTop').fadeOut();
		}
	});
	
	//Click event to scroll to top
	$('.scrollToTop').click(function(){
		$('html, body').animate({scrollTop : 0},800);
		return false;
	});
	
	$('.next_select').click(function(){
		if ($('html, body').width() < 360) {
			$('.content_inr').toggle();
		} else {
			$('.content_inr').css('display' , 'block');
		}
	});
	 $('.setting').click(function(){
            $(".setting_information").toggle();
           
        });
		//edit_profile
		//hart_like
		$('.fa.fa-heart-o').click(function(){
			$('.fa.fa-heart').show();
	    });
		$('.fa.fa-heart').click(function(){
			$('.fa.fa-heart').hide();
	    });
		$('.clint_edit_profile li').click(function(){
			$(this).addClass("active_button");
	    });
		$('.edit_profile').click(function(){
            $(".clint_about").hide();
			$(".clint_edit_profile").show();
			$(".edit_profile").css('color' , '#333');
			$(".save_cheng").css('display' , 'block');
			$(".edit_profile").css('display' , 'none');
           
        });
		$('.save_cheng').click(function(){
            $(".clint_about").show();
			$(".clint_edit_profile").hide();
			$(".save_cheng").css('display' , 'none');
			$(".edit_profile").css('display' , 'block');
        });
		$('.edit02').click(function(){
            $(".work02").show();
			$(".info02").hide();
			$(".save02").show();
			$(".edit02").hide();
        });
		$('.save02').click(function(){
            $(".work02").hide();
			$(".info02").show();
			$(".save02").hide();
        });
		$('.edit03').click(function(){
            $(".work03").show();
			$(".info03").hide();
			$(".save03").show();
			$(".edit03").hide();
        });
		$('.save03').click(function(){
            $(".work03").hide();
			$(".info03").show();
			$(".save03").hide();
        });
		$('.edit01').click(function(){
            $(".work01").show();
			$(".info01").hide();
			$(".save01").show();
			$(".edit01").hide();
        });
		$('.save01').click(function(){
            $(".work01").hide();
			$(".info01").show();
			$(".save01").hide();
        });
		//profile_img_on click function
		//$('.profile_pick_landing').click(function(){
//			$('.img_about').hide();
//           $(this).find('.img_about').toggle();
//        });
		//profile_img_on click function
		//popup function
	 $('[data-popup-open]').on('click', function(e){
        var targeted_popup_class = jQuery(this).attr('data-popup-open');
        $('[data-popup="' + targeted_popup_class + '"]').fadeIn(350);
        e.preventDefault();
    });
    //----- CLOSE
    $('[data-popup-close]').on('click', function(e){
        var targeted_popup_class = jQuery(this).attr('data-popup-close');
        $('[data-popup="' + targeted_popup_class + '"]').fadeOut(350);
        e.preventDefault();
    });
	
	//setting switch
	$('.Switch').click(function() {
		$(this).toggleClass('On').toggleClass('Off');
		});
	
	$('.load').click(function(){
		$('.more_mutual_hangout').toggle();
		return false;
	});
	$(".menu_btn").click(function() {
		$(".immigration_section .right").toggleClass("active")

	});
	$("body").click(function() {
		$(".immigration_section .right").removeClass("active")

	});
	$(".immigration_section .right,.menu_btn").click(function(e){
		e.stopImmediatePropagation();
	});

     $('.chat-listinginactive').toggle(function(){
         $('.conv-list-view').addClass("active-users");
         $('.chat-view').addClass("inactive-users");
         $('.window').addClass("fullwidth");
         $('.chat-view').removeClass('active-chat');
         $('.conv-list-view').removeClass("hide-users");
         $('.chat-listinginactive').trigger('click');
     },function(){
         $('.conv-list-view').removeClass("active-users");
         $('.chat-view').removeClass("inactive-users");
         $('.window').removeClass("fullwidth");
     });
    $('.conv-list li').click(function(){
        $(this).toggleClass("selected");
        $(this).siblings().removeClass("selected");
        $('.chat-view').addClass('active-chat');
        $('.conv-list-view').addClass("hide-users");
        $('.conv-list-view').removeClass("active-users");
        $('.chat-view').removeClass("inactive-users");
        $('.window').removeClass("fullwidth");

        var windowwidth = $(window).width();
        if(windowwidth > 319 || windowwidth < 767)
        {
            var navbar = $('.orange-header').height();
            var chatmsgContainer = $('.chat-view__input').outerHeight(true);//height of chat msg input
            var chatmsgHeader = $('.chat-view__header').outerHeight();//height of chat header
            var windowsize = $(window).height();//browser viewport size
            var windowHeight = windowsize - navbar; //height of the msgs container
            var messageviewHeight = windowHeight - chatmsgContainer - chatmsgHeader;
            $('.message-view').css('height',messageviewHeight);
            scrollBottom();
        }
    });
    $('.my_window .conv-list li').click(function(){
        $(this).toggleClass("selected");
        $(this).siblings().removeClass("selected");
        $('.my_window .chat-view').addClass('active-chat');
        $('.my_window .conv-list-view').addClass("hide-users");
        $('.my_window .conv-list-view').removeClass("active-users");
        $('.my_window .chat-view').removeClass("inactive-users");
        $('.my_window').removeClass("fullwidth");

        var windowwidth = $(window).width();
        if(windowwidth > 319 || windowwidth < 767)
        {
            var navbar = $('.orange-header').height();
            var chatmsgContainer = $('.my_window .chat-view__input').outerHeight(true);//height of chat msg input
            var chatmsgHeader = $('.my_window .chat-view__header').outerHeight();//height of chat header
            var windowsize = $(window).height();//browser viewport size
            var windowHeight = windowsize - navbar; //height of the msgs container
            var messageviewHeight = windowHeight - chatmsgContainer - chatmsgHeader;
            $('.my_window .message-view').css('height',messageviewHeight);
        }
    });

    var navbar = $('.orange-header').height();
    var chatmsgContainer = $('.chat-view__input').outerHeight(true);//height of chat msg input
    var chatmsgHeader = $('.chat-view__header').outerHeight();//height of chat header
    var windowsize = $(window).height();//browser viewport size
    var windowHeight = windowsize - navbar; //height of the msgs container
    var messageviewHeight = windowHeight - chatmsgContainer - chatmsgHeader;//to provide scroll and show input msgr

    $('.window').css('height',windowHeight);
    $('.message-view').css('height',messageviewHeight);
    $(".nano").nanoScroller();

    var windowwidth = $(window).width();
    var mobileresponsive = windowHeight - $('.conv-list-view__header').outerHeight() - $('.search-left').outerHeight();
    $('.conv-list').css('height',mobileresponsive);

    $(".fa-comment").click(function(e){
     $('.window').css('display','none');
     $('.my_window').css('display','block');
     var mobileresponsive = windowHeight - $('.conv-list-view__header.notificatin_hed').outerHeight() - $('.my_window .search-left').outerHeight();
     $('.my_window .conv-list').css('height',mobileresponsive);
    });

    $(".fa-arrow-left").click(function(e){
     $('.window').css('display','block');
     $('.my_window').css('display','none');
    });
    document.getElementById('texttype').addEventListener('keyup', function () {
     this.style.height = 0;
     this.style.height = this.scrollHeight + 'px';
    }, false);
    document.getElementById('texttype2').addEventListener('keyup', function () {
         this.style.height = 0;
         this.style.height = this.scrollHeight + 'px';
    }, false);

    $('.txt1').focus(function () {
        $(this).css('border','1px solid #e5e5e5');
        this.style.height = 0;
        this.style.height = this.scrollHeight + 'px';
    });
    $('.txt1').blur(function () {
        $(this).css('border','none');
        $(this).css('height', '30px');
    });
    $(document).ready(function(){
     scrollBottom();
    });
    function scrollBottom()
    {
     $('.msgswrapper').animate({scrollTop: $('.msgswrapper')[0].scrollHeight}, 1000);
    }
	
});