const { createApp } = Vue;

createApp({
    data() {
        return {
            data: null,
            loading: false,
            error: null
        }
    },
    methods: {
        async fetchData() {
            this.loading = true;
            this.data = null;
            this.error = null;

            try {
                const response = await fetch('/api/data');
                if (!response.ok) throw new Error('Ошибка сети');
                this.data = await response.json();
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        }
    },
    mounted() {
        console.log("Vue приложение запущено!");
    }
}).mount('#app');