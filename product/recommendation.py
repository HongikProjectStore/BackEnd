def get_unseen_product(ratings_matrix, userId):
    user_rating = ratings_matrix.loc[userId,:]
    already_seen = user_rating[user_rating>0].index.tolist()
    products_list = ratings_matrix.columns.tolist()
    unseen_list = [ product for product in products_list if product not in already_seen]
    return unseen_list

def recommend_product_by_userid(pred_df, userId, unseen_list, top_n = 10):
    recomm_products = pred_df.loc[userId,unseen_list].sort_values(ascending=False)[:top_n]
    return recomm_products