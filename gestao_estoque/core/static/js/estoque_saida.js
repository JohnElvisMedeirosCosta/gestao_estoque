$(document).ready(function(){
    // Insere classe no primeiro item de produto
    $('#id_estoque-0-produto').addClass('clProduto')
    $('#id_estoque-0-quantidade').addClass('clQuantidade')
    // Desabilita o primeiro campo 'saldo'
    $('#id_estoque-0-saldo').prop('type', 'hidden')
    // Cria um span para mostrar o saldo na tela.
    $('label[for="id_estoque-0-saldo"]').append('<span id="id_estoque-0-saldo-span" class="lead" style="padding-left:10px;"></span>')
    // Criar um campo com o estoque inicial
    $('label[for="id_estoque-0-saldo"]').append('<input id="id_estoque-0-inicial" class="form-control" type="hidden" />')
    // Select2
    $('.clProduto').select2()
});
$('#add-item').click(function(ev){
    ev.preventDefault();
    var count = $('#estoque').children().length;
    var tmplMarkup = $('#item-estoque').html();
    var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
    $('div#estoque').append(compiledTmpl);

    // update form count
    $('#id_estoque-TOTAL_FORMS').val(count + 1)

    // Desabilita o primeiro campo 'saldo'
    $('#id_estoque-'+(count)+'-saldo').prop('type', 'hidden')

    // some animate to scroll to view our new form
    $('html, body').animate({
        scrollTop: $('#item-' + count).offset().top
    }, 1000);
    $('#id_estoque-' + count + '-produto').addClass('clProduto')
    $('#id_estoque-' + count + '-quantidade').addClass('clQuantidade')
    // Cria um span para mostrar o saldo na tela.
    $('label[for="id_estoque-' + count + '-saldo"]').append('<span id="id_estoque-' + count + '-saldo-span" class="lead" style="padding-left:10px;"></span>')
    // Criar um campo com o estoque inicial
    $('label[for="id_estoque-' + count + '-saldo"]').append('<input id="id_estoque-' + count + '-inicial" class="form-control" type="hidden" />')
    $('.clProduto').select2()
});

let estoque;
let saldo;
let campo;
let quantidade;
let campo2;

$(document).on('change', '.clProduto', function () {
    let self = $(this)
    let pk = $(this).val()
    let url = '/produto/' + pk + '/json/'

    $.ajax({
        url:url,
        type: 'GET',
        success: function (response) {
            estoque = response.data[0].estoque
            campo = self.attr('id').replace('produto', 'quantidade')
            estoque_inicial = self.attr('id').replace('produto', 'inicial')
            // Estoque inicial
            $('#' + estoque_inicial).val(estoque)
            // Remover o valor do campo 'quantidade'
            $('#' + campo).val('')
        },
        error: function(xhr) {
            //body...
        }
    })
});

$(document).on('change', '.clQuantidade', function () {
    quantidade = $(this).val()
    campo = $(this).attr('id').replace('quantidade', 'saldo')
    campo_estoque_incial = $(this).attr('id').replace('quantidade', 'inicial')
    estoque_inicial = $('#' + campo_estoque_incial).val()
    saldo = Number(estoque_inicial) - Number(quantidade)
    if (saldo < 0) {
        alert('Quantidade maior que o saldo em estoque!')
        $('#' + campo).val('')
        return false
    }
    // Desabilita o 'saldo'
    $('#' + campo).prop('type', 'hidden')
    //Atribui o saldo ao campo 'saldo'
    $('#' + campo).val(saldo)
    campo2 = $(this).attr('id').replace('quantidade', 'saldo-span')
    // Atribui o saldo ao campo 'id_estoque-x-saldo-span'
    $('#' + campo2).text(saldo)
});