# Skybound Ruins

Platformer escrito em Python com PgZero. O projeto carrega o mapa a partir de `map.txt`, renderiza sprites animados para o herói e inimigos, e oferece mecânica de combate simples com salto duplo.

## Requisitos

- Python 3.11+
- PgZero (`pip install pgzero`)

O jogo usa apenas `pgzero`, `random` e `pygame.Rect` (disponível ao instalar PgZero).

## Como rodar

```bash
pip install pgzero
pgzrun game.py
```

Os recursos de imagem e som já estão no repositório (pastas `images/` e `sounds/`). O arquivo `map.txt` pode ser editado para ajustar plataformas e spawns (`1` = bloco, `P` = herói, `E` = inimigo).

## Controles

| Ação            | Tecla                   |
|-----------------|------------------------|
| Mover           | `←`/`→` ou `A`/`D`      |
| Pular / Double Jump | `↑` ou `W`            |
| Ataque          | `Space`, `Z`, `X`, `K`  |
| Pausa / Menu    | `Esc`                   |
| Confirmar (menus) | `Enter`                |

## Estados do jogo

- **Menu**: título, opções de iniciar, ligar/desligar som e sair.
- **Jogando**: herói com salto duplo; inimigos patrulham as plataformas do mapa.
- **Vitória**: exibida quando todos os inimigos caem; botão “Restart” reinicia.
- **Game Over**: ao perder todas as vidas; `Restart` ou `Esc` para voltar ao menu.

## Estrutura

- `game.py` – lógica principal, carregamento do mapa e estados do jogo.
- `map.txt` – layout do nível (32×24 tiles).
- `images/` & `sounds/` – assets usados pelo PgZero.

