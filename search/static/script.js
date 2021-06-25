
$(document).ready(
	
	function() {
		
		$("form[name=loginform]").on(
			"submit",
			function( event ) {
				if( $("input[name=user_id]").val() == "" ) {
					alert( "아이디를 입력하세요" )
					return false
				}
				if( $("input[name=password]").val() == "" ) {
					alert( "비밀번호를 입력하세요" )
					return false
				}
			}
		)
				
		$("form[name=passform]").on(
			"submit",
			function( event ) {
				if( $("input[name=password]").val() == "" ) {
					alert( "비밀번호를 입력하세요" )
					return false
				}	
			}
		)
		
		$("#emailresult").html( "&nbsp;이메일을 입력하세요" )
		$("input[name=email]").on(
			"keyup",
			function( event ) {
				$.ajax(
					{
						url : "emailcheck",
						type : "POST",																		
						data : {
							keyword : $("input[name=email]").val(),
						},
						dataType : "text",
						success : function( data ) {
							$("#emailresult").html( "&nbsp;" + data )
						},
						error : function() {							
						}
					}							
				)				
			}
		)
		$("#telresult").html( "&nbsp;-는 제외하고 입력하세요" )
		$("input[name=hp]").on(
			"keydown",
			function( event ) {		
				$("#telresult").html( "&nbsp;전화번호 형식에 맞지않습니다" )
			}
		)
		
		
	}	
)

function setid( id ) {
	opener.document.registerform.user_id.value = id
	self.close()
}

function setemail( email ) {
	opener.document.registerform.email.value = email
	self.close()
}















