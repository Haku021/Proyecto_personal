document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.btn-incrementar').forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);
            const max = parseInt(input.getAttribute('max'));
            let valor = parseInt(input.value);
            
            if (valor < max) {
                input.value = valor + 1;
            }
        });
    });
    document.querySelectorAll('.btn-decrementar').forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);
            const min = parseInt(input.getAttribute('min'));
            let valor = parseInt(input.value);
            
            if (valor > min) {
                input.value = valor - 1;
            }
        });
    });
});