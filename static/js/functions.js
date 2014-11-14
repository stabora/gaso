$(document).ready(function() {
	$('textarea[name=texto]').focus();

	$('form[name=gaso-form]').bootstrapValidator(
	{
		feedbackIcons:
		{
			valid: 'glyphicon glyphicon-ok',
			invalid: 'glyphicon glyphicon-remove',
			validating: 'glyphicon glyphicon-refresh'
		},

		fields:
		{
			texto: { validators: { notEmpty: { message: 'Ingregasese un tegasexto para continuagasar' } } }
		}
	});
});