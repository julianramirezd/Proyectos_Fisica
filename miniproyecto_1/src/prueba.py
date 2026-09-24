import numpy as np
import pandas as pd
from scipy import stats


def probar_equiprobabilidad(df_o_hits, nivel_significancia=0.05):
    """Realiza la prueba de hipótesis de equiprobabilidad usando Chi-Cuadrado,

    compatible con cualquier versión de SciPy.
    """
    # 1. Extracción de los hits observados
    if isinstance(df_o_hits, pd.DataFrame):
        df_agrupado = (
            df_o_hits.groupby("Configuracion")["Hits"].sum().reset_index()
        )
        configuraciones = df_agrupado["Configuracion"].tolist()
        hits_observados = df_agrupado["Hits"].to_numpy()
    elif isinstance(df_o_hits, dict):
        configuraciones = list(df_o_hits.keys())
        hits_observados = np.array(list(df_o_hits.values()))
    else:
        hits_observados = np.array(df_o_hits)
        configuraciones = [f"Config_{i+1}" for i in range(len(hits_observados))]

    total_hits = np.sum(hits_observados)
    k = len(hits_observados)

    if total_hits == 0:
        print(
            "⚠️ ADVERTENCIA: El número total de Hits es 0. No se puede realizar la prueba."
        )
        return {"p_valor": None, "decision": "Sin Datos"}

    # 2. Frecuencias esperadas bajo H0 (Equiprobabilidad: p = 1/k)
    prob_teorica = [1.0 / k] * k
    hits_esperados = np.array([total_hits / k] * k)

    # 3. Prueba Chi-Cuadrado (Estándar y compatible)
    chi2_stat, p_valor = stats.chisquare(
        f_obs=hits_observados, f_exp=hits_esperados
    )

    # 4. Toma de Decisión
    rechazar_h0 = p_valor <= nivel_significancia
    decision = (
        "SE RECHAZA H0 (No hay Equiprobabilidad)"
        if rechazar_h0
        else "NO SE RECHAZA H0 (Equiprobable)"
    )

    # 5. Tabla Resumen
    df_resumen = pd.DataFrame(
        {
            "Configuración": configuraciones,
            "Hits Observados": hits_observados,
            "Hits Esperados (H0)": np.round(hits_esperados, 2),
            "Prob. Observada": np.round(hits_observados / total_hits, 4)
            if total_hits > 0
            else 0,
            "Prob. Teórica (H0)": np.round(prob_teorica, 4),
        }
    )

    print("=" * 60)
    print("      PRUEBA DE HIPÓTESIS DE EQUIPROBABILIDAD DE ESTADOS")
    print("=" * 60)
    print(df_resumen.to_string(index=False))
    print("-" * 60)
    print(f"Total de Hits Evaluados (N) : {total_hits}")
    print(
        f"Prueba Chi-Cuadrado (χ²)    : Estadística = {chi2_stat:.4f}, p-valor = {p_valor:.4f}"
    )
    print(f"Nivel de Significancia (α)  : {nivel_significancia}")
    print(f"Veredicto Final             : {decision}")
    print("=" * 60)

    return {
        "df_resumen": df_resumen,
        "p_valor": p_valor,
        "chi2_stat": chi2_stat,
        "rechazar_h0": rechazar_h0,
        "decision": decision,
    }
